from ashare_strategy.core.config import StrategyConfig, AccountConfig
from ashare_strategy.accounts.providers.router import build_account_repository


def test_build_json_account_repository():
    cfg = StrategyConfig(account=AccountConfig(provider='json', position_store_path='data/test.json'))
    repo = build_account_repository(cfg)
    assert repo is not None
