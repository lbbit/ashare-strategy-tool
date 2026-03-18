from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import typer
from rich import print
from rich.table import Table

from ashare_strategy.core.config import load_config
from ashare_strategy.execution.portfolio import TradingService

app = typer.Typer(help="A股策略选股/回测工具")


@app.command()
def screen(config: str = typer.Option("config/default_strategy.yaml", help="配置文件路径")):
    cfg = load_config(config)
    service = TradingService(cfg)
    df = service.screen()
    if df.empty:
        print("[yellow]没有筛选到符合条件的股票[/yellow]")
        return
    table = Table(title="候选股票")
    for col in df.columns:
        table.add_column(str(col))
    for _, row in df.iterrows():
        table.add_row(*[str(v) for v in row.tolist()])
    print(table)


@app.command()
def backtest(config: str = typer.Option("config/default_strategy.yaml"), initial_capital: float = 1_000_000):
    cfg = load_config(config)
    service = TradingService(cfg)
    result = service.backtest(initial_capital=initial_capital)
    print_json = json.dumps(result, ensure_ascii=False, indent=2, default=str)
    print(print_json)


@app.command()
def ui():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/ashare_strategy/ui/app.py"], check=False)


if __name__ == "__main__":
    app()
