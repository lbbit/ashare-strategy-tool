from __future__ import annotations

from ashare_strategy.accounts.models import Holding
from ashare_strategy.accounts.repository import AccountRepository


class ManualAccountRepository(AccountRepository):
    def __init__(self, holdings: list[Holding] | None = None) -> None:
        self._holdings = holdings or []

    def load_holdings(self) -> list[Holding]:
        return self._holdings

    def save_holdings(self, holdings: list[Holding]) -> None:
        self._holdings = holdings
