from __future__ import annotations

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.data.providers.router import build_data_provider
from ashare_strategy.services.backtest import BacktestService
from ashare_strategy.services.portfolio import PortfolioService
from ashare_strategy.services.screening import ScreeningService


class TradingService:
    def __init__(self, config: StrategyConfig) -> None:
        self.provider = build_data_provider(config)
        self.config = config
        self.screening_service = ScreeningService(self.provider, config)
        self.backtest_service = BacktestService(self.provider, config)
        self.portfolio_service = PortfolioService(config)

    def screen(self):
        return self.screening_service.run()

    def backtest(self, initial_capital: float = 1_000_000, mode: str = "rolling"):
        return self.backtest_service.run(initial_capital=initial_capital, mode=mode)

    def load_positions(self):
        return self.portfolio_service.load_positions()

    def save_positions(self, positions: list[dict]):
        self.portfolio_service.save_positions(positions)
