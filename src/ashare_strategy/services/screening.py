from __future__ import annotations

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.data.providers.base import MarketDataProvider
from ashare_strategy.strategies.selector import StrategySelector


class ScreeningService:
    def __init__(self, provider: MarketDataProvider, config: StrategyConfig) -> None:
        self.provider = provider
        self.config = config

    def run(self):
        return StrategySelector(self.provider, self.config).select_candidates()
