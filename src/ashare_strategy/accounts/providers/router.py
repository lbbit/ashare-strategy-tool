from __future__ import annotations

from ashare_strategy.accounts.providers.json_store import JsonAccountRepository
from ashare_strategy.accounts.providers.manual import ManualAccountRepository
from ashare_strategy.accounts.repository import AccountRepository
from ashare_strategy.core.config import StrategyConfig


def build_account_repository(config: StrategyConfig) -> AccountRepository:
    provider = config.account.provider
    if provider == 'json':
        return JsonAccountRepository(config.account.position_store_path)
    if provider == 'manual':
        return ManualAccountRepository()
    raise ValueError(f'不支持的账户提供者: {provider}')
