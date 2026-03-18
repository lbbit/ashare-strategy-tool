from ashare_strategy.core.config import StrategyConfig


def test_config_defaults():
    cfg = StrategyConfig()
    assert cfg.max_positions == 3
    assert cfg.hold_days == 5
