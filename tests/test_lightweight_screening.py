import pandas as pd

from ashare_strategy.core.config import StrategyConfig, DataSourceConfig
from ashare_strategy.data.providers.router import build_data_provider
from ashare_strategy.strategies.selector import StrategySelector


class DummyTinyProvider:
    def capabilities(self):
        return {
            'spot': False,
            'board_names': False,
            'board_hist': False,
            'board_cons': False,
            'daily': True,
            'benchmark_daily': True,
            'trade_range': True,
            'lightweight_screen': True,
        }

    def get_stock_daily(self, symbol, start_date=None, end_date=None):
        rows = []
        for i in range(38):
            rows.append({'date': f'2026-02-{(i % 20) + 1:02d}', 'open': 10.0, 'close': 10.1, 'high': 10.2, 'low': 9.9, 'volume': 900, 'pct_chg': 0.5})
        rows.append({'date': '2026-03-17', 'open': 10.0, 'close': 10.8, 'high': 11.0, 'low': 9.9, 'volume': 1000, 'pct_chg': 8.0})
        rows.append({'date': '2026-03-18', 'open': 10.9, 'close': 11.2, 'high': 11.3, 'low': 10.8, 'volume': 1200, 'pct_chg': 2.0})
        return pd.DataFrame(rows).assign(date=lambda df: pd.to_datetime(df['date']))

    def get_spot(self):
        return pd.DataFrame()

    def get_benchmark_daily(self, symbol='sh000300'):
        return pd.DataFrame()

    def get_board_names(self):
        return pd.DataFrame()

    def get_board_hist(self, board_name):
        return pd.DataFrame()

    def get_board_cons(self, board_name):
        return pd.DataFrame()

    def get_recent_trade_range(self, days=365):
        return ('2025-01-01', '2026-03-18')


def test_lightweight_selector_returns_candidates():
    selector = StrategySelector(DummyTinyProvider(), StrategyConfig())
    result = selector.select_candidates()
    assert not result.empty
    assert 'stock_code' in result.columns
