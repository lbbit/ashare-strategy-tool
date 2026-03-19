from __future__ import annotations

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.data.providers.akshare import AkshareProvider
from ashare_strategy.data.providers.base import MarketDataProvider


def build_data_provider(config: StrategyConfig) -> MarketDataProvider:
    provider_name = getattr(config, 'data_provider', 'akshare')
    if provider_name == 'akshare':
        return AkshareProvider(cache_dir=config.data_cache_dir, use_cache=config.use_cache)
    raise ValueError(f'不支持的数据源: {provider_name}')
