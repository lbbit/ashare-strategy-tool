from pathlib import Path

from ashare_strategy.accounts.models import Holding
from ashare_strategy.accounts.providers.json_store import JsonAccountRepository


def test_json_account_repository(tmp_path: Path):
    repo = JsonAccountRepository(str(tmp_path / 'positions.json'))
    repo.save_holdings([Holding(stock_code='000001', stock_name='A', shares=100)])
    holdings = repo.load_holdings()
    assert holdings[0].stock_code == '000001'
    assert holdings[0].shares == 100
