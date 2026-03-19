from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.templates import export_template_configs


def test_export_template_configs(tmp_path):
    files = export_template_configs(StrategyConfig(), tmp_path)
    assert len(files) == 3
    assert (tmp_path / 'beginner_strategy.yaml').exists()
