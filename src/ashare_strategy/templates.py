from __future__ import annotations

from pathlib import Path

import yaml

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


def export_template_configs(base_config: StrategyConfig, output_dir: str | Path) -> list[str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for name in TEMPLATE_PRESETS:
        cfg = apply_template(base_config, name)
        file_path = out / f'{name}_strategy.yaml'
        file_path.write_text(yaml.safe_dump(cfg.model_dump(mode='python'), allow_unicode=True, sort_keys=False), encoding='utf-8')
        files.append(str(file_path))
    return files
