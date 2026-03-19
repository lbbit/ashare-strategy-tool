from __future__ import annotations

from ashare_strategy.accounts.models import Holding
from ashare_strategy.accounts.providers.json_store import JsonAccountRepository
from ashare_strategy.core.config import StrategyConfig


class PortfolioService:
    def __init__(self, config: StrategyConfig) -> None:
        self.repository = JsonAccountRepository(config.position_store_path)

    def load_positions(self):
        return [item.model_dump() for item in self.repository.load_holdings()]

    def save_positions(self, positions: list[dict]):
        holdings = [Holding(**item) for item in positions]
        self.repository.save_holdings(holdings)
