from __future__ import annotations

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.data.providers.akshare import AkshareProvider
from ashare_strategy.data.providers.base import MarketDataProvider
from ashare_strategy.data.providers.tushare import TushareProvider


def build_data_provider(config: StrategyConfig) -> MarketDataProvider:
    provider_name = getattr(config, 'data_provider', 'akshare')
    if provider_name == 'akshare':
        return AkshareProvider(cache_dir=config.data_cache_dir, use_cache=config.use_cache, timeout_seconds=config.data_source.timeout_seconds, max_retries=config.data_source.max_retries)
    if provider_name == 'tushare':
        if not config.data_source.tushare_token:
            raise ValueError('使用 tushare 数据源时必须配置 data_source.tushare_token')
        return TushareProvider(token=config.data_source.tushare_token, cache_dir=config.data_cache_dir, use_cache=config.use_cache)
    raise ValueError(f'不支持的数据源: {provider_name}')
