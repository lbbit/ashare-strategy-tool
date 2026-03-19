from pathlib import Path

from ashare_strategy.core.config import load_config


def test_load_legacy_flat_config(tmp_path: Path):
    cfg_file = tmp_path / 'legacy.yaml'
    cfg_file.write_text('data_provider: akshare\ndata_cache_dir: cache_dir\nuse_cache: false\nposition_store_path: data/test.json\n', encoding='utf-8')
    cfg = load_config(cfg_file)
    assert cfg.data_source.provider == 'akshare'
    assert cfg.data_source.cache_dir == 'cache_dir'
    assert cfg.data_source.use_cache is False
    assert cfg.account.position_store_path == 'data/test.json'
