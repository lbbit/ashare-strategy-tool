from __future__ import annotations

from ashare_strategy.accounts.models import AccountSnapshot, Holding
from ashare_strategy.accounts.providers.router import build_account_repository
from ashare_strategy.core.config import StrategyConfig


class PortfolioService:
    def __init__(self, config: StrategyConfig) -> None:
        self.repository = build_account_repository(config)

    def load_positions(self):
        return [item.model_dump() for item in self.repository.load_holdings()]

    def load_account(self) -> dict:
        positions = self.load_positions()
        cash = 0.0
        market_value = 0.0
        for item in positions:
            price = item.get("latest_price") or item.get("buy_price") or 0.0
            shares = item.get("shares") or 0
            market_value += float(price) * int(shares)
        snapshot = AccountSnapshot(cash=cash, market_value=market_value, total_asset=cash + market_value, positions=[Holding(**item) for item in positions])
        return snapshot.model_dump()

    def save_positions(self, positions: list[dict]):
        holdings = [Holding(**item) for item in positions]
        self.repository.save_holdings(holdings)
