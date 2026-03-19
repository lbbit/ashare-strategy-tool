from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass
class ProviderHealthCheck:
    provider: str
    sdk: str = ""
    status: str = "unknown"
    auth_ok: bool = False
    cache_enabled: bool = False
    checks: list[dict[str, Any]] | None = None
    message: str = ""

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["checks"] = data.get("checks") or []
        return data
