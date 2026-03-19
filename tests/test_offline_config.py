from ashare_strategy.core.config import load_config


def test_offline_mode_legacy_field(tmp_path):
    p = tmp_path / 'cfg.yaml'
    p.write_text('offline_mode: true\n', encoding='utf-8')
    cfg = load_config(p)
    assert cfg.data_source.offline_mode is True
