from __future__ import annotations

import pandas as pd


def result_to_dataframes(result: dict) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    candidates = pd.DataFrame(result.get("candidates", []))
    trades = pd.DataFrame(result.get("trades", []))
    equity = pd.DataFrame(result.get("equity_curve", []))
    if not equity.empty:
        equity["date"] = pd.to_datetime(equity["date"])
    return candidates, trades, equity
