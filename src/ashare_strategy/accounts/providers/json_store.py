from __future__ import annotations

from ashare_strategy.accounts.models import Holding
from ashare_strategy.accounts.repository import AccountRepository
from ashare_strategy.execution.state import PositionStore


class JsonAccountRepository(AccountRepository):
    def __init__(self, path: str) -> None:
        self.store = PositionStore(path)

    def load_holdings(self) -> list[Holding]:
        return [Holding(**item) for item in self.store.load()]

    def save_holdings(self, holdings: list[Holding]) -> None:
        self.store.save([item.model_dump() for item in holdings])
