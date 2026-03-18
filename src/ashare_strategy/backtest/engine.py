from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta

import pandas as pd

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.core.models import Position
from ashare_strategy.data.provider import AkshareProvider
from ashare_strategy.strategies.selector import StrategySelector


class SimpleBacktester:
    def __init__(self, provider: AkshareProvider, config: StrategyConfig) -> None:
        self.provider = provider
        self.config = config

    def run(self, initial_capital: float = 1_000_000) -> dict:
        selector = StrategySelector(self.provider, self.config)
        candidates = selector.select_candidates()
        positions: list[Position] = []
        trades = []
        cash = initial_capital
        equity = initial_capital

        for _, row in candidates.iterrows():
            if len(positions) >= self.config.max_positions:
                break
            alloc = equity / self.config.max_positions
            shares = alloc / row["second_day_open"]
            positions.append(Position(
                stock_code=row["stock_code"],
                stock_name=row["stock_name"],
                buy_date=row["trade_date"],
                buy_price=row["second_day_open"],
                shares=shares,
                first_day_open=row["first_day_open"],
            ))
            cash -= alloc
            trades.append({"action": "BUY", "date": row["trade_date"], "code": row["stock_code"], "price": row["second_day_open"], "shares": shares})

        for pos in list(positions):
            df = self.provider.get_stock_daily(pos.stock_code)
            df["ma5"] = df["close"].rolling(self.config.sell_ma_window).mean()
            df = df[df["date"] >= pd.to_datetime(pos.buy_date)].reset_index(drop=True)
            sell_row = None
            for i, r in df.iterrows():
                holding_days = i + 1
                if r["close"] < r["ma5"] or r["close"] < pos.first_day_open or holding_days >= self.config.hold_days:
                    sell_row = r
                    pos.holding_days = holding_days
                    break
            if sell_row is None:
                sell_row = df.iloc[-1]
                pos.holding_days = len(df)
            proceeds = pos.shares * float(sell_row["close"])
            cash += proceeds
            trades.append({"action": "SELL", "date": str(sell_row["date"].date()), "code": pos.stock_code, "price": float(sell_row["close"]), "shares": pos.shares, "holding_days": pos.holding_days})

        equity = cash
        benchmark = self.provider.get_benchmark_daily(self.config.benchmark_symbol)
        if len(benchmark) >= 2:
            bench_ret = benchmark.iloc[-1]["close"] / benchmark.iloc[max(0, len(benchmark) - 252)]["close"] - 1 if len(benchmark) > 252 else benchmark.iloc[-1]["close"] / benchmark.iloc[0]["close"] - 1
        else:
            bench_ret = 0.0
        strategy_ret = equity / initial_capital - 1
        return {
            "initial_capital": initial_capital,
            "final_equity": equity,
            "strategy_return": strategy_ret,
            "benchmark_return": float(bench_ret),
            "excess_return": strategy_ret - float(bench_ret),
            "trades": trades,
            "candidates": candidates.to_dict(orient="records"),
        }
