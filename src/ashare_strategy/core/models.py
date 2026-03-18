from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CandidateSignal:
    trade_date: str
    stock_code: str
    stock_name: str
    board_name: str
    float_shares: float
    first_day_open: float
    first_day_close: float
    second_day_open: float
    second_day_close: float


@dataclass
class Position:
    stock_code: str
    stock_name: str
    buy_date: str
    buy_price: float
    shares: float
    first_day_open: float
    holding_days: int = 0
