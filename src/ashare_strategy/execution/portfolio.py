from __future__ import annotations

from ashare_strategy.backtest.engine import SimpleBacktester
from ashare_strategy.backtest.rolling_engine import RollingBacktester
from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.data.provider import AkshareProvider
from ashare_strategy.strategies.selector import StrategySelector


class TradingService:
    def __init__(self, config: StrategyConfig) -> None:
        self.provider = AkshareProvider(cache_dir=config.data_cache_dir, use_cache=config.use_cache)
        self.config = config

    def screen(self):
        return StrategySelector(self.provider, self.config).select_candidates()

    def backtest(self, initial_capital: float = 1_000_000, mode: str = "rolling"):
        if mode == "simple":
            return SimpleBacktester(self.provider, self.config).run(initial_capital=initial_capital)
        return RollingBacktester(self.provider, self.config).run(initial_capital=initial_capital)
