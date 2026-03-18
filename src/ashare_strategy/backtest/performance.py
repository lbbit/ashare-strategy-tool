from __future__ import annotations

import math

import pandas as pd


def summarize_performance(equity_curve: list[dict], trades: list[dict], benchmark_return: float = 0.0) -> dict:
    equity = pd.DataFrame(equity_curve)
    if equity.empty or len(equity) < 2:
        return {
            "annualized_return": 0.0,
            "volatility": 0.0,
            "sharpe_ratio": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "profit_loss_ratio": 0.0,
            "benchmark_return": benchmark_return,
        }

    equity["daily_return"] = equity["equity"].pct_change().fillna(0.0)
    total_return = equity.iloc[-1]["equity"] / equity.iloc[0]["equity"] - 1
    periods = max(1, len(equity))
    annualized_return = (1 + total_return) ** (252 / periods) - 1 if total_return > -1 else -1.0
    volatility = equity["daily_return"].std(ddof=0) * math.sqrt(252)
    sharpe = annualized_return / volatility if volatility > 0 else 0.0
    equity["peak"] = equity["equity"].cummax()
    equity["drawdown"] = equity["equity"] / equity["peak"] - 1
    max_dd = float(equity["drawdown"].min())

    pnl_list = []
    open_buys = {}
    for trade in trades:
        if trade.get("action") == "BUY":
            open_buys[trade["code"]] = trade
        elif trade.get("action") == "SELL" and trade.get("code") in open_buys:
            buy = open_buys.pop(trade["code"])
            pnl = (trade["price"] - buy["price"]) * trade["shares"]
            pnl_list.append(pnl)
    wins = [x for x in pnl_list if x > 0]
    losses = [abs(x) for x in pnl_list if x < 0]
    win_rate = len(wins) / len(pnl_list) if pnl_list else 0.0
    profit_loss_ratio = (sum(wins) / len(wins)) / (sum(losses) / len(losses)) if wins and losses else 0.0

    return {
        "annualized_return": float(annualized_return),
        "volatility": float(volatility),
        "sharpe_ratio": float(sharpe),
        "max_drawdown": max_dd,
        "win_rate": float(win_rate),
        "profit_loss_ratio": float(profit_loss_ratio),
        "benchmark_return": float(benchmark_return),
    }
