from __future__ import annotations

from ashare_strategy.core.config import StrategyConfig


TEMPLATE_PRESETS = {
    'beginner': {
        'lookback_days': 365,
        'max_positions': 3,
        'hold_days': 5,
        'rebalance_interval': 7,
        'first_day_gain_pct': 7.0,
    },
    'conservative': {
        'lookback_days': 500,
        'max_positions': 2,
        'hold_days': 7,
        'rebalance_interval': 10,
        'first_day_gain_pct': 5.0,
    },
    'aggressive': {
        'lookback_days': 240,
        'max_positions': 5,
        'hold_days': 3,
        'rebalance_interval': 5,
        'first_day_gain_pct': 8.0,
    },
}


def apply_template(config: StrategyConfig, template_name: str) -> StrategyConfig:
    preset = TEMPLATE_PRESETS.get(template_name)
    if not preset:
        return config
    data = config.model_dump()
    data.update(preset)
    return StrategyConfig(**data)
