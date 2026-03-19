from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd


class MarketDataProvider(ABC):
    @abstractmethod
    def get_stock_daily(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_spot(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_benchmark_daily(self, symbol: str = "sh000300") -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_board_names(self) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_board_hist(self, board_name: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_board_cons(self, board_name: str) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def get_recent_trade_range(self, days: int = 365) -> tuple[str, str]:
        raise NotImplementedError
