from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.templates import apply_template


def test_apply_conservative_template():
    cfg = apply_template(StrategyConfig(), 'conservative')
    assert cfg.max_positions == 2
    assert cfg.hold_days == 7
