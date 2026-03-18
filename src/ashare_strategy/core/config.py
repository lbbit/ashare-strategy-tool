from __future__ import annotations

from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class StrategyConfig(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    lookback_days: int = 365
    rebalance_interval: int = 7
    max_positions: int = 3
    max_daily_buys: int = 3
    equal_weight: bool = True
    board_ma_window: int = 250
    board_volume_days: int = 5
    board_min_volume: float = 120
    stock_float_cap_max: float = 1_000_000_000
    first_day_gain_pct: float = 7.0
    second_day_open_gap_positive: bool = True
    second_day_bullish: bool = True
    buy_ma_window: int = 20
    sell_ma_window: int = 5
    hold_days: int = 5
    benchmark_symbol: str = "sh000300"
    exclude_st: bool = True
    board_name_keywords: list[str] = Field(default_factory=list)


def load_config(path: str | Path | None = None) -> StrategyConfig:
    if not path:
        return StrategyConfig()
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return StrategyConfig(**data)
