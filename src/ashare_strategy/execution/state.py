from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class PositionStore:
    def __init__(self, path: str = "data/positions.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, positions: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(positions, ensure_ascii=False, indent=2), encoding="utf-8")
