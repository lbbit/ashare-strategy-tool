from __future__ import annotations

from abc import ABC, abstractmethod

from ashare_strategy.accounts.models import Holding


class AccountRepository(ABC):
    @abstractmethod
    def load_holdings(self) -> list[Holding]:
        raise NotImplementedError

    @abstractmethod
    def save_holdings(self, holdings: list[Holding]) -> None:
        raise NotImplementedError
