from __future__ import annotations

from pathlib import Path
from typing import Callable

import pandas as pd


class CsvCache:
    def __init__(self, base_dir: str = ".cache/market_data", enabled: bool = True) -> None:
        self.base_dir = Path(base_dir)
        self.enabled = enabled
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def load_or_fetch(self, key: str, fetcher: Callable[[], pd.DataFrame]) -> pd.DataFrame:
        path = self.base_dir / f"{key}.csv"
        if self.enabled and path.exists():
            return pd.read_csv(path)
        df = fetcher()
        if self.enabled and not df.empty:
            df.to_csv(path, index=False)
        return df
