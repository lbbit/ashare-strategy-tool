from ashare_strategy.core.config import StrategyConfig, DataSourceConfig
from ashare_strategy.data.providers.router import build_data_provider


def test_build_tushare_provider():
    cfg = StrategyConfig(data_source=DataSourceConfig(provider='tushare', tushare_token='token'))
    provider = build_data_provider(cfg)
    assert provider is not None
