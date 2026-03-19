from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_report(result: dict, output_dir: str = 'reports') -> dict:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    candidates = pd.DataFrame(result.get('candidates', []))
    trades = pd.DataFrame(result.get('trades', []))
    equity = pd.DataFrame(result.get('equity_curve', []))
    metrics = pd.DataFrame([{
        'strategy_return': result.get('strategy_return', 0),
        'benchmark_return': result.get('benchmark_return', 0),
        'excess_return': result.get('excess_return', 0),
        'max_drawdown': result.get('max_drawdown', 0),
        'annualized_return': result.get('annualized_return', 0),
        'volatility': result.get('volatility', 0),
        'sharpe_ratio': result.get('sharpe_ratio', 0),
        'win_rate': result.get('win_rate', 0),
        'profit_loss_ratio': result.get('profit_loss_ratio', 0),
    }])
    files = {
        'candidates': out / 'candidates.csv',
        'trades': out / 'trades.csv',
        'equity_curve': out / 'equity_curve.csv',
        'metrics': out / 'metrics.csv',
    }
    candidates.to_csv(files['candidates'], index=False)
    trades.to_csv(files['trades'], index=False)
    equity.to_csv(files['equity_curve'], index=False)
    metrics.to_csv(files['metrics'], index=False)
    return {k: str(v) for k, v in files.items()}
