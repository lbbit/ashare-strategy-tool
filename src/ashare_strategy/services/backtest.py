from __future__ import annotations

from ashare_strategy.backtest.engine import SimpleBacktester
from ashare_strategy.backtest.rolling_engine import RollingBacktester
from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.data.providers.base import MarketDataProvider


class BacktestService:
    def __init__(self, provider: MarketDataProvider, config: StrategyConfig) -> None:
        self.provider = provider
        self.config = config

    def run(self, initial_capital: float = 1_000_000, mode: str = 'rolling'):
        if mode == 'simple':
            return SimpleBacktester(self.provider, self.config).run(initial_capital=initial_capital)
        return RollingBacktester(self.provider, self.config).run(initial_capital=initial_capital)
