from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

import pandas as pd

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.core.models import CandidateSignal
from ashare_strategy.data.provider import AkshareProvider


class StrategySelector:
    def __init__(self, provider: AkshareProvider, config: StrategyConfig) -> None:
        self.provider = provider
        self.config = config
        caps = provider.capabilities() if hasattr(provider, 'capabilities') else {}
        self.capabilities = caps
        self.spot = provider.get_spot() if caps.get('spot') else pd.DataFrame(columns=['代码', '名称', '流通股'])

    def _is_st(self, name: str) -> bool:
        return "ST" in str(name).upper()

    def _board_pass(self, board_df: pd.DataFrame) -> bool:
        if len(board_df) < self.config.board_ma_window:
            return False
        df = board_df.copy()
        df["ma250"] = df["close"].rolling(self.config.board_ma_window).mean()
        latest = df.iloc[-1]
        recent_vol = df["volume"].tail(self.config.board_volume_days)
        return bool(latest["close"] > latest["ma250"] and (recent_vol > self.config.board_min_volume).all())

    def _board_filter(self, boards: Iterable[str]) -> list[str]:
        passed = []
        for board in boards:
            if self.config.board_name_keywords and not any(k in board for k in self.config.board_name_keywords):
                continue
            try:
                hist = self.provider.get_board_hist(board)
                if self._board_pass(hist):
                    passed.append(board)
            except Exception:
                continue
        return passed

    def _find_stock_signal(self, code: str, name: str, board_name: str) -> CandidateSignal | None:
        if self.config.exclude_st and self._is_st(name):
            return None
        spot_match = self.spot[self.spot["代码"] == code] if not self.spot.empty and "代码" in self.spot.columns else pd.DataFrame()
        if spot_match.empty:
            float_shares = 0.0
        else:
            float_shares = pd.to_numeric(spot_match.iloc[0].get("流通股", None), errors="coerce")
            if pd.isna(float_shares):
                float_shares = 0.0
        if float_shares and float_shares >= self.config.stock_float_cap_max:
            return None
        try:
            daily = self.provider.get_stock_daily(code)
        except Exception:
            return None
        if len(daily) < max(30, self.config.buy_ma_window + 2):
            return None
        daily = daily.copy()
        daily["ma20"] = daily["close"].rolling(self.config.buy_ma_window).mean()
        prev = daily.iloc[-2]
        last = daily.iloc[-1]
        prev_gain_ok = prev["pct_chg"] >= self.config.first_day_gain_pct and prev["close"] > prev["open"]
        last_gap_ok = (not self.config.second_day_open_gap_positive) or (last["open"] > prev["close"])
        last_bull_ok = (not self.config.second_day_bullish) or (last["close"] > last["open"] and last["volume"] > prev["volume"])
        buy_ok = last["open"] > prev["close"] and last["open"] > last["ma20"]
        if prev_gain_ok and last_gap_ok and last_bull_ok and buy_ok:
            return CandidateSignal(
                trade_date=str(last["date"].date()),
                stock_code=code,
                stock_name=name,
                board_name=board_name,
                float_shares=float(float_shares),
                first_day_open=float(prev["open"]),
                first_day_close=float(prev["close"]),
                second_day_open=float(last["open"]),
                second_day_close=float(last["close"]),
            )
        return None

    def _select_board_candidates(self) -> pd.DataFrame:
        boards_df = self.provider.get_board_names()
        board_col = "板块名称" if "板块名称" in boards_df.columns else boards_df.columns[0]
        passed_boards = self._board_filter(boards_df[board_col].tolist())
        candidates: list[dict] = []
        for board in passed_boards:
            try:
                cons = self.provider.get_board_cons(board)
            except Exception:
                continue
            code_col = "代码" if "代码" in cons.columns else cons.columns[1]
            name_col = "名称" if "名称" in cons.columns else cons.columns[2]
            for _, row in cons.iterrows():
                signal = self._find_stock_signal(str(row[code_col]).zfill(6), str(row[name_col]), board)
                if signal:
                    candidates.append(asdict(signal))
        df = pd.DataFrame(candidates)
        if df.empty:
            return df
        return df.sort_values("float_shares").head(self.config.max_positions).reset_index(drop=True)

    def _select_lightweight_candidates(self) -> pd.DataFrame:
        sample_universe = [
            ("000001", "平安银行", "核心观察池"),
            ("000333", "美的集团", "核心观察池"),
            ("000651", "格力电器", "核心观察池"),
            ("600036", "招商银行", "核心观察池"),
            ("600519", "贵州茅台", "核心观察池"),
            ("600900", "长江电力", "核心观察池"),
            ("601318", "中国平安", "核心观察池"),
            ("300750", "宁德时代", "核心观察池"),
        ]
        candidates: list[dict] = []
        for code, name, board_name in sample_universe:
            try:
                daily = self.provider.get_stock_daily(code)
            except Exception:
                continue
            if len(daily) < max(30, self.config.buy_ma_window + 2):
                continue
            daily = daily.copy()
            daily["ma20"] = daily["close"].rolling(self.config.buy_ma_window).mean()
            prev = daily.iloc[-2]
            last = daily.iloc[-1]
            prev_gain_ok = prev["pct_chg"] >= self.config.first_day_gain_pct and prev["close"] > prev["open"]
            last_gap_ok = (not self.config.second_day_open_gap_positive) or (last["open"] >= prev["close"])
            last_bull_ok = (not self.config.second_day_bullish) or (last["close"] > last["open"])
            buy_ok = last["open"] >= last["ma20"]
            if prev_gain_ok and last_gap_ok and last_bull_ok and buy_ok:
                candidates.append(asdict(CandidateSignal(
                    trade_date=str(last["date"].date()),
                    stock_code=code,
                    stock_name=name,
                    board_name=board_name,
                    float_shares=0.0,
                    first_day_open=float(prev["open"]),
                    first_day_close=float(prev["close"]),
                    second_day_open=float(last["open"]),
                    second_day_close=float(last["close"]),
                )))
        df = pd.DataFrame(candidates)
        if df.empty:
            return df
        return df.head(self.config.max_positions).reset_index(drop=True)

    def select_candidates(self) -> pd.DataFrame:
        if self.capabilities.get('board_names') and self.capabilities.get('board_cons'):
            return self._select_board_candidates()
        if self.capabilities.get('lightweight_screen'):
            return self._select_lightweight_candidates()
        return pd.DataFrame()
