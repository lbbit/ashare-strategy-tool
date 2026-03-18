import pandas as pd

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.strategies.selector import StrategySelector


class DummyProvider:
    def get_spot(self):
        return pd.DataFrame([{"代码": "000001", "流通股": 500000000}])


def test_st_check():
    selector = StrategySelector(DummyProvider(), StrategyConfig())
    assert selector._is_st("ST测试") is True
    assert selector._is_st("平安银行") is False
