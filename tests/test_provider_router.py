from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.data.providers.router import build_data_provider


def test_build_default_provider():
    provider = build_data_provider(StrategyConfig())
    assert provider is not None
