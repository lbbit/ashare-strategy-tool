from ashare_strategy.reporting import export_report


def test_export_report(tmp_path):
    result = {
        'candidates': [{'stock_code': '000001'}],
        'trades': [{'action': 'BUY', 'code': '000001'}],
        'equity_curve': [{'date': '2026-01-01', 'equity': 100}],
        'strategy_return': 0.1,
    }
    files = export_report(result, str(tmp_path))
    assert (tmp_path / 'candidates.csv').exists()
    assert 'metrics' in files
