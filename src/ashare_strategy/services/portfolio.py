from __future__ import annotations

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.execution.state import PositionStore


class PortfolioService:
    def __init__(self, config: StrategyConfig) -> None:
        self.store = PositionStore(config.position_store_path)

    def load_positions(self):
        return self.store.load()

    def save_positions(self, positions: list[dict]):
        self.store.save(positions)
