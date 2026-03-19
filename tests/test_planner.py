from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.planner import TradingPlanner


class DummyService:
    def screen(self):
        import pandas as pd
        return pd.DataFrame([
            {'stock_code': '000001', 'stock_name': 'A'},
            {'stock_code': '000002', 'stock_name': 'B'},
        ])

    def load_positions(self):
        return [{'stock_code': '000001', 'stock_name': 'A', 'shares': 100}]


def test_build_daily_plan():
    planner = TradingPlanner(DummyService(), StrategyConfig())
    result = planner.build_daily_plan()
    assert result['summary']['buy_count'] == 1
    assert result['summary']['hold_count'] == 1
