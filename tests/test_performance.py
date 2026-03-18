from ashare_strategy.backtest.performance import summarize_performance


def test_summarize_performance_basic():
    equity = [
        {"date": "2026-01-01", "equity": 100000},
        {"date": "2026-01-02", "equity": 101000},
        {"date": "2026-01-03", "equity": 102000},
    ]
    trades = [
        {"action": "BUY", "code": "000001", "price": 10, "shares": 100},
        {"action": "SELL", "code": "000001", "price": 11, "shares": 100},
    ]
    result = summarize_performance(equity, trades, benchmark_return=0.01)
    assert result["max_drawdown"] <= 0
    assert result["win_rate"] == 1.0
    assert result["profit_loss_ratio"] == 0.0
