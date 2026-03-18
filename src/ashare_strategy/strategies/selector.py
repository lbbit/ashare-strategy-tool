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
        self.spot = provider.get_spot()

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
        spot_match = self.spot[self.spot["代码"] == code]
        if spot_match.empty:
            return None
        float_shares = pd.to_numeric(spot_match.iloc[0].get("流通股", None), errors="coerce")
        if pd.isna(float_shares) or float_shares >= self.config.stock_float_cap_max:
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

    def select_candidates(self) -> pd.DataFrame:
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
