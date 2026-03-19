from __future__ import annotations

from pydantic import BaseModel


class Holding(BaseModel):
    stock_code: str
    stock_name: str = ""
    buy_date: str | None = None
    buy_price: float | None = None
    shares: int = 0
    available_shares: int | None = None
    latest_price: float | None = None
    target_weight: float | None = None


class AccountSnapshot(BaseModel):
    cash: float = 0.0
    total_asset: float | None = None
    market_value: float | None = None
    positions: list[Holding] = []
