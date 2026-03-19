from __future__ import annotations

from ashare_strategy.data.provider import AkshareProvider as _AkshareProvider


class AkshareProvider(_AkshareProvider):
    def capabilities(self) -> dict[str, bool]:
        caps = super().capabilities() if hasattr(super(), 'capabilities') else {}
        caps.update({
            "spot": True,
            "board_names": True,
            "board_hist": True,
            "board_cons": True,
            "daily": True,
            "benchmark_daily": True,
            "trade_range": True,
            "lightweight_screen": True,
        })
        return caps


__all__ = ["AkshareProvider"]
