from __future__ import annotations

from pydantic import BaseModel


class Holding(BaseModel):
    stock_code: str
    stock_name: str = ""
    buy_date: str | None = None
    buy_price: float | None = None
    shares: int = 0
