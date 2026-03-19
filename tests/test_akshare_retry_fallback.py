from pathlib import Path

import pandas as pd

from ashare_strategy.data.provider import AkshareProvider


def test_retry_falls_back_to_cache(tmp_path: Path):
    provider = AkshareProvider(cache_dir=str(tmp_path), use_cache=True, max_retries=0)
    cache_file = Path(tmp_path) / 'demo.csv'
    pd.DataFrame([{'a': 1}]).to_csv(cache_file, index=False)
    result = provider._with_retry('demo', lambda: (_ for _ in ()).throw(RuntimeError('boom')))
    assert result.iloc[0]['a'] == 1
