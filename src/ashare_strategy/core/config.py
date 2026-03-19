from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class StrategyConfig(BaseModel):
    data_provider: str = "akshare"
    data_cache_dir: str = ".cache/market_data"
    use_cache: bool = True
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
    commission_rate: float = 0.0003
    stamp_duty_rate: float = 0.001
    slippage_rate: float = 0.0005
    position_store_path: str = "data/positions.json"


def resolve_config_path(path: str | Path | None = None) -> Path | None:
    if not path:
        return None
    candidate = Path(path)
    if candidate.exists():
        return candidate
    if getattr(sys, "frozen", False):
        bundle_dir = Path(getattr(sys, "_MEIPASS", Path(sys.executable).resolve().parent))
        bundled_candidate = bundle_dir / Path(path)
        if bundled_candidate.exists():
            return bundled_candidate
        exe_relative_candidate = Path(sys.executable).resolve().parent / Path(path)
        if exe_relative_candidate.exists():
            return exe_relative_candidate
    project_relative = Path(__file__).resolve().parents[3] / Path(path)
    if project_relative.exists():
        return project_relative
    return candidate


def load_config(path: str | Path | None = None) -> StrategyConfig:
    if not path:
        return StrategyConfig()
    resolved = resolve_config_path(path)
    if resolved is None:
        return StrategyConfig()
    data = yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}
    return StrategyConfig(**data)
