from __future__ import annotations

from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional

import pandas as pd


class AkshareProvider:
    def __init__(self) -> None:
        self._ak = None

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
        ak = self._akshare()
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", adjust="qfq")
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
        ak = self._akshare()
        return ak.stock_zh_a_spot_em()

    def get_benchmark_daily(self, symbol: str = "sh000300") -> pd.DataFrame:
        ak = self._akshare()
        df = ak.index_zh_a_hist(symbol=symbol, period="daily")
        df = df.rename(columns={"日期": "date", "开盘": "open", "收盘": "close", "最高": "high", "最低": "low", "成交量": "volume"})
        return self._normalize_dates(df)

    def get_board_names(self) -> pd.DataFrame:
        try:
            ak = self._akshare()
            return ak.stock_board_industry_name_em()
        except Exception:
            return pd.DataFrame(columns=["板块名称"])

    def get_board_hist(self, board_name: str) -> pd.DataFrame:
        ak = self._akshare()
        df = ak.stock_board_industry_hist_em(symbol=board_name, adjust="")
        df = df.rename(columns={"日期": "date", "开盘": "open", "收盘": "close", "最高": "high", "最低": "low", "成交量": "volume"})
        return self._normalize_dates(df)

    def get_board_cons(self, board_name: str) -> pd.DataFrame:
        ak = self._akshare()
        return ak.stock_board_industry_cons_em(symbol=board_name)

    def get_recent_trade_range(self, days: int = 365) -> tuple[str, str]:
        end = datetime.today().date()
        start = end - timedelta(days=days * 2)
        return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
