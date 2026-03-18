from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional

import pandas as pd

from ashare_strategy.data.cache import CsvCache


class AkshareProvider:
    def __init__(self, cache_dir: str = ".cache/market_data", use_cache: bool = True) -> None:
        self._ak = None
        self.cache = CsvCache(cache_dir, enabled=use_cache)

    def _akshare(self):
        if self._ak is None:
            import akshare as ak
            self._ak = ak
        return self._ak

    @staticmethod
    def _normalize_dates(df: pd.DataFrame, date_col: str = "date") -> pd.DataFrame:
        out = df.copy()
        out[date_col] = pd.to_datetime(out[date_col])
        out = out.sort_values(date_col).reset_index(drop=True)
        return out

    def get_stock_daily(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        def fetch():
            ak = self._akshare()
            return ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
        df = self.cache.load_or_fetch(f"stock_daily_{symbol}", fetch)
        rename_map = {"日期": "date", "开盘": "open", "收盘": "close", "最高": "high", "最低": "low", "成交量": "volume", "涨跌幅": "pct_chg", "换手率": "turnover"}
        df = df.rename(columns=rename_map)
        df = self._normalize_dates(df)
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        return df.reset_index(drop=True)

    @lru_cache(maxsize=1)
    def get_spot(self) -> pd.DataFrame:
        return self.cache.load_or_fetch("stock_spot", lambda: self._akshare().stock_zh_a_spot_em())

    def get_benchmark_daily(self, symbol: str = "sh000300") -> pd.DataFrame:
        df = self.cache.load_or_fetch(f"benchmark_{symbol}", lambda: self._akshare().index_zh_a_hist(symbol=symbol, period="daily"))
        df = df.rename(columns={"日期": "date", "开盘": "open", "收盘": "close", "最高": "high", "最低": "low", "成交量": "volume"})
        return self._normalize_dates(df)

    def get_board_names(self) -> pd.DataFrame:
        try:
            return self.cache.load_or_fetch("board_names", lambda: self._akshare().stock_board_industry_name_em())
        except Exception:
            return pd.DataFrame(columns=["板块名称"])

    def get_board_hist(self, board_name: str) -> pd.DataFrame:
        df = self.cache.load_or_fetch(f"board_hist_{board_name}", lambda: self._akshare().stock_board_industry_hist_em(symbol=board_name, adjust=""))
        df = df.rename(columns={"日期": "date", "开盘": "open", "收盘": "close", "最高": "high", "最低": "low", "成交量": "volume"})
        return self._normalize_dates(df)

    def get_board_cons(self, board_name: str) -> pd.DataFrame:
        return self.cache.load_or_fetch(f"board_cons_{board_name}", lambda: self._akshare().stock_board_industry_cons_em(symbol=board_name))

    def get_recent_trade_range(self, days: int = 365) -> tuple[str, str]:
        end = datetime.today().date()
        start = end - timedelta(days=days * 2)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
