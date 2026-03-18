from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict
from datetime import datetime, timedelta

import pandas as pd

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.core.models import Position
from ashare_strategy.data.provider import AkshareProvider
from ashare_strategy.strategies.selector import StrategySelector


class RollingBacktester:
    def __init__(self, provider: AkshareProvider, config: StrategyConfig) -> None:
        self.provider = provider
        self.config = config

    def _date_range(self) -> tuple[pd.Timestamp, pd.Timestamp]:
        end = pd.Timestamp.today().normalize() if not self.config.end_date else pd.Timestamp(self.config.end_date)
        start = end - pd.Timedelta(days=self.config.lookback_days) if not self.config.start_date else pd.Timestamp(self.config.start_date)
        return start, end

    def run(self, initial_capital: float = 1_000_000) -> dict:
        selector = StrategySelector(self.provider, self.config)
        candidates = selector.select_candidates()
        start, end = self._date_range()
        benchmark = self.provider.get_benchmark_daily(self.config.benchmark_symbol)
        benchmark = benchmark[(pd.to_datetime(benchmark["date"]) >= start) & (pd.to_datetime(benchmark["date"]) <= end)].copy()
        if benchmark.empty:
            return {"error": "benchmark data unavailable"}
        trade_dates = pd.to_datetime(benchmark["date"]).dt.normalize().tolist()

        cash = initial_capital
        positions: dict[str, Position] = {}
        trades = []
        equity_curve = []
        stock_data = {}
        next_rebalance_idx = 0

        for code in candidates.get("stock_code", pd.Series(dtype=str)).tolist():
            df = self.provider.get_stock_daily(code)
            if not df.empty:
                df = df.copy()
                df["date"] = pd.to_datetime(df["date"]).dt.normalize()
                df["ma5"] = df["close"].rolling(self.config.sell_ma_window).mean()
                stock_data[code] = df.set_index("date")

        for i, current_date in enumerate(trade_dates):
            # sell checks
            for code in list(positions.keys()):
                pos = positions[code]
                sdf = stock_data.get(code)
                if sdf is None or current_date not in sdf.index:
                    continue
                row = sdf.loc[current_date]
                pos.holding_days += 1
                if row["close"] < row["ma5"] or row["close"] < pos.first_day_open or pos.holding_days >= self.config.hold_days:
                    proceeds = pos.shares * float(row["close"])
                    cash += proceeds
                    trades.append({"action": "SELL", "date": str(current_date.date()), "code": code, "price": float(row["close"]), "shares": pos.shares, "holding_days": pos.holding_days})
                    del positions[code]

            # rebalance / buy checks
            if i >= next_rebalance_idx:
                next_rebalance_idx = i + self.config.rebalance_interval
                buy_list = []
                for _, row in candidates.iterrows():
                    code = row["stock_code"]
                    if code in positions or len(positions) + len(buy_list) >= self.config.max_positions:
                        continue
                    sdf = stock_data.get(code)
                    if sdf is None or current_date not in sdf.index:
                        continue
                    mrow = sdf.loc[current_date]
                    buy_ok = mrow["open"] > row["first_day_close"] and (pd.isna(mrow.get("ma20", float('nan'))) or True)
                    if buy_ok:
                        buy_list.append((row, mrow))
                    if len(buy_list) >= self.config.max_daily_buys:
                        break
                slots = max(1, self.config.max_positions)
                alloc_per_trade = cash / max(1, min(slots, len(buy_list))) if buy_list else 0
                for row, mrow in buy_list:
                    if alloc_per_trade <= 0:
                        continue
                    shares = alloc_per_trade / float(mrow["open"])
                    positions[row["stock_code"]] = Position(
                        stock_code=row["stock_code"],
                        stock_name=row["stock_name"],
                        buy_date=str(current_date.date()),
                        buy_price=float(mrow["open"]),
                        shares=shares,
                        first_day_open=float(row["first_day_open"]),
                    )
                    cash -= alloc_per_trade
                    trades.append({"action": "BUY", "date": str(current_date.date()), "code": row["stock_code"], "price": float(mrow["open"]), "shares": shares})

            market_value = 0.0
            for code, pos in positions.items():
                sdf = stock_data.get(code)
                if sdf is not None and current_date in sdf.index:
                    market_value += pos.shares * float(sdf.loc[current_date]["close"])
            equity_curve.append({"date": str(current_date.date()), "equity": cash + market_value})

        final_equity = equity_curve[-1]["equity"] if equity_curve else initial_capital
        benchmark_return = float(benchmark.iloc[-1]["close"] / benchmark.iloc[0]["close"] - 1)
        strategy_return = float(final_equity / initial_capital - 1)
        equity_df = pd.DataFrame(equity_curve)
        equity_df["peak"] = equity_df["equity"].cummax()
        equity_df["drawdown"] = equity_df["equity"] / equity_df["peak"] - 1
        return {
            "initial_capital": initial_capital,
            "final_equity": final_equity,
            "strategy_return": strategy_return,
            "benchmark_return": benchmark_return,
            "excess_return": strategy_return - benchmark_return,
            "max_drawdown": float(equity_df["drawdown"].min()) if not equity_df.empty else 0.0,
            "trade_count": len(trades),
            "trades": trades,
            "candidates": candidates.to_dict(orient="records"),
            "equity_curve": equity_curve,
        }
