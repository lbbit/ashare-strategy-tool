from __future__ import annotations

import pandas as pd


def result_to_dataframes(result: dict):
    candidates = pd.DataFrame(result.get("candidates", []))
    trades = pd.DataFrame(result.get("trades", []))
    equity = pd.DataFrame(result.get("equity_curve", []))
    return candidates, trades, equity


SCHEMA_VERSION = "1.0"


def success_response(data, message: str = "ok"):
    return {"schema_version": SCHEMA_VERSION, "status": "success", "message": message, "data": data}


def error_response(message: str, data=None):
    return {"schema_version": SCHEMA_VERSION, "status": "error", "message": message, "data": data}
