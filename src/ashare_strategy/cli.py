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
from ashare_strategy.data.providers.router import build_data_provider
from ashare_strategy.data.diagnostics import build_provider_diagnostics, format_provider_hint
from ashare_strategy.reporting import export_report
from ashare_strategy.planner import TradingPlanner
from ashare_strategy.utils import success_response, error_response
from ashare_strategy.templates import apply_template, TEMPLATE_PRESETS, export_template_configs

app = typer.Typer(help="A股策略选股/回测工具")


@app.command()
def screen(config: str = typer.Option("config/default_strategy.yaml", help="配置文件路径"), output: str = typer.Option("table", help="输出格式：table/json"), template: str = typer.Option("", help="策略模板：beginner/conservative/aggressive"), offline: bool = typer.Option(False, help="仅使用缓存/离线模式")):
    cfg = load_config(config)
    if offline:
        cfg.data_source.offline_mode = True
    if template:
        cfg = apply_template(cfg, template)
    service = TradingService(cfg)
    df = service.screen()
    if output == "json":
        print(json.dumps(success_response(df.to_dict(orient="records"), message="screen completed"), ensure_ascii=False, indent=2, default=str))
        return
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
def backtest(config: str = typer.Option("config/default_strategy.yaml"), initial_capital: float = 1_000_000, mode: str = typer.Option("rolling", help="rolling/simple"), export_csv: str = typer.Option("", help="导出交易结果 CSV 路径"), export_report_dir: str = typer.Option("", help="导出完整报告目录"), output: str = typer.Option("text", help="输出格式：text/json"), template: str = typer.Option("", help="策略模板：beginner/conservative/aggressive"), offline: bool = typer.Option(False, help="仅使用缓存/离线模式")):
    cfg = load_config(config)
    if offline:
        cfg.data_source.offline_mode = True
    if template:
        cfg = apply_template(cfg, template)
    service = TradingService(cfg)
    try:
        result = service.backtest(initial_capital=initial_capital, mode=mode)
    except Exception as e:
        diag = build_provider_diagnostics(cfg)
        hint = format_provider_hint(diag)
        if output == "json":
            print(json.dumps(error_response(f"{e}", {"provider_diagnostics": diag, "hint": hint}), ensure_ascii=False, indent=2, default=str))
        else:
            print(f"[red]回测失败：{e}[/red]")
            print(f"[yellow]{hint}[/yellow]")
            print("[yellow]建议先执行：ashare-strategy doctor-data[/yellow]")
        raise typer.Exit(code=1)
    print_json = json.dumps(result, ensure_ascii=False, indent=2, default=str)
    if output == "json":
        print(json.dumps(success_response(result, message="backtest completed"), ensure_ascii=False, indent=2, default=str))
    else:
        print(print_json)
    if export_csv:
        import pandas as pd
        pd.DataFrame(result.get("trades", [])).to_csv(export_csv, index=False)
        print(f"[green]交易结果已导出到 {export_csv}[/green]")
    if export_report_dir:
        files = export_report(result, export_report_dir)
        print(f"[green]完整报告已导出: {files}[/green]")


@app.command()
def plan(config: str = typer.Option("config/default_strategy.yaml"), output_dir: str = typer.Option("daily_plan", help="导出交易计划目录"), output: str = typer.Option("text", help="输出格式：text/json"), template: str = typer.Option("", help="策略模板：beginner/conservative/aggressive"), offline: bool = typer.Option(False, help="仅使用缓存/离线模式")):
    cfg = load_config(config)
    if offline:
        cfg.data_source.offline_mode = True
    if template:
        cfg = apply_template(cfg, template)
    service = TradingService(cfg)
    planner = TradingPlanner(service, cfg)
    try:
        result = planner.export_daily_plan(output_dir)
    except Exception as e:
        diag = build_provider_diagnostics(cfg)
        hint = format_provider_hint(diag)
        if output == "json":
            print(json.dumps(error_response(str(e), {"provider_diagnostics": diag, "hint": hint}), ensure_ascii=False, indent=2, default=str))
        else:
            print(f"[red]生成交易计划失败：{e}[/red]")
            print(f"[yellow]{hint}[/yellow]")
            print("[yellow]建议先执行：ashare-strategy doctor-data[/yellow]")
        raise typer.Exit(code=1)
    if output == "json":
        print(json.dumps(success_response(result['plan'], message="plan generated"), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(result['plan'], ensure_ascii=False, indent=2))
        print(f"[green]交易计划已导出到 {result['output_dir']}[/green]")


@app.command()
def positions(config: str = typer.Option("config/default_strategy.yaml"), output: str = typer.Option("text", help="输出格式：text/json")):
    cfg = load_config(config)
    service = TradingService(cfg)
    data = service.load_positions()
    if output == "json":
        print(json.dumps(success_response(data, message="positions loaded"), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


@app.command()
def save_sample_positions(config: str = typer.Option("config/default_strategy.yaml"), output: str = typer.Option("text", help="输出格式：text/json")):
    cfg = load_config(config)
    service = TradingService(cfg)
    sample = [{"stock_code": "000001", "stock_name": "示例股票", "buy_date": "2026-03-18", "buy_price": 12.34, "shares": 1000}]
    service.save_positions(sample)
    if output == "json":
        print(json.dumps(success_response(sample, message="sample positions saved"), ensure_ascii=False, indent=2))
    else:
        print("[green]已写入示例持仓[/green]")


@app.command()
def init_account(config: str = typer.Option("config/default_strategy.yaml"), output: str = typer.Option("text", help="输出格式：text/json")):
    cfg = load_config(config)
    service = TradingService(cfg)
    sample = [{"stock_code": "000001", "stock_name": "示例股票", "buy_date": "2026-03-18", "buy_price": 12.34, "shares": 1000}]
    service.save_positions(sample)
    if output == "json":
        print(json.dumps(success_response(sample, message="account initialized"), ensure_ascii=False, indent=2))
    else:
        print("[green]已初始化示例持仓文件，可按需修改为你的真实持仓[/green]")


@app.command()
def init_workspace(
    config: str = typer.Option("config/default_strategy.yaml"),
    output_dir: str = typer.Option("workspace_init", help="初始化输出目录"),
    output: str = typer.Option("text", help="输出格式：text/json")
):
    cfg = load_config(config)
    service = TradingService(cfg)
    sample = [{"stock_code": "000001", "stock_name": "示例股票", "buy_date": "2026-03-18", "buy_price": 12.34, "shares": 1000}]
    service.save_positions(sample)
    from pathlib import Path
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    reports_dir = out / "reports"
    plans_dir = out / "daily_plan"
    reports_dir.mkdir(exist_ok=True)
    plans_dir.mkdir(exist_ok=True)
    (out / "README.txt").write_text("这是初始化后的工作目录。你可以在这里保存报告、计划和自定义文件。", encoding="utf-8")
    (out / "custom_strategy.yaml").write_text(Path(config).read_text(encoding="utf-8"), encoding="utf-8")
    template_files = export_template_configs(cfg, out)
    payload = {"positions_initialized": True, "output_dir": str(out), "files": [str(out / "README.txt"), str(out / "custom_strategy.yaml"), *template_files], "directories": [str(reports_dir), str(plans_dir)]}
    if output == "json":
        print(json.dumps(success_response(payload, message="workspace initialized"), ensure_ascii=False, indent=2))
    else:
        print(f"[green]已完成初始化：持仓模板已写入，工作目录已创建 -> {out}[/green]")


@app.command("doctor-data")
def doctor_data(config: str = typer.Option("config/default_strategy.yaml", help="配置文件路径"), output: str = typer.Option("text", help="输出格式：text/json")):
    cfg = load_config(config)
    provider = build_data_provider(cfg)
    if not hasattr(provider, 'health_check'):
        payload = error_response('当前数据源暂不支持健康检查')
        if output == 'json':
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print('[yellow]当前数据源暂不支持健康检查[/yellow]')
        raise typer.Exit(code=1)
    result = provider.health_check().to_dict()
    wrapped = success_response(result, message='data provider health checked')
    if output == 'json':
        print(json.dumps(wrapped, ensure_ascii=False, indent=2, default=str))
        return
    print(f"[bold]数据源:[/bold] {result['provider']}  SDK: {result.get('sdk') or '-'}")
    print(f"[bold]状态:[/bold] {result['status']}  | 缓存启用: {result['cache_enabled']}")
    print(f"[bold]说明:[/bold] {result['message']}")
    table = Table(title='数据源健康检查')
    table.add_column('检查项')
    table.add_column('状态')
    table.add_column('说明')
    for item in result.get('checks', []):
        table.add_row(str(item.get('name')), str(item.get('status')), str(item.get('message', item.get('rows', ''))))
    print(table)


@app.command()
def ui():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "src/ashare_strategy/ui/app.py"], check=False)


if __name__ == "__main__":
    app()
