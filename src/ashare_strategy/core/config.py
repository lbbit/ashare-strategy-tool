from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field


class DataSourceConfig(BaseModel):
    provider: str = "akshare"
    cache_dir: str = ".cache/market_data"
    use_cache: bool = True
    timeout_seconds: int = 20
    max_retries: int = 2
    tushare_token: str = ""


class AccountConfig(BaseModel):
    provider: str = "json"
    position_store_path: str = "data/positions.json"


class AppConfig(BaseModel):
    default_output: str = "text"


class StrategyConfig(BaseModel):
    data_source: DataSourceConfig = Field(default_factory=DataSourceConfig)
    account: AccountConfig = Field(default_factory=AccountConfig)
    app: AppConfig = Field(default_factory=AppConfig)
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

    @property
    def data_provider(self) -> str:
        return self.data_source.provider

    @property
    def data_cache_dir(self) -> str:
        return self.data_source.cache_dir

    @property
    def use_cache(self) -> bool:
        return self.data_source.use_cache

    @property
    def account_provider(self) -> str:
        return self.account.provider

    @property
    def position_store_path(self) -> str:
        return self.account.position_store_path


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
    if 'data_provider' in data or 'data_cache_dir' in data or 'use_cache' in data or 'tushare_token' in data or 'timeout_seconds' in data or 'max_retries' in data:
        data.setdefault('data_source', {})
        if 'data_provider' in data:
            data['data_source']['provider'] = data.pop('data_provider')
        if 'data_cache_dir' in data:
            data['data_source']['cache_dir'] = data.pop('data_cache_dir')
        if 'use_cache' in data:
            data['data_source']['use_cache'] = data.pop('use_cache')
        if 'tushare_token' in data:
            data['data_source']['tushare_token'] = data.pop('tushare_token')
        if 'timeout_seconds' in data:
            data['data_source']['timeout_seconds'] = data.pop('timeout_seconds')
        if 'max_retries' in data:
            data['data_source']['max_retries'] = data.pop('max_retries')
    if 'account_provider' in data or 'position_store_path' in data:
        data.setdefault('account', {})
        if 'account_provider' in data:
            data['account']['provider'] = data.pop('account_provider')
        if 'position_store_path' in data:
            data['account']['position_store_path'] = data.pop('position_store_path')
    return StrategyConfig(**data)
