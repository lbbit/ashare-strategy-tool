from __future__ import annotations

from ashare_strategy.accounts.models import Holding
from ashare_strategy.accounts.providers.router import build_account_repository
from ashare_strategy.core.config import StrategyConfig


class PortfolioService:
    def __init__(self, config: StrategyConfig) -> None:
        self.repository = build_account_repository(config)

    def load_positions(self):
        return [item.model_dump() for item in self.repository.load_holdings()]

    def save_positions(self, positions: list[dict]):
        holdings = [Holding(**item) for item in positions]
        self.repository.save_holdings(holdings)
