from typer.testing import CliRunner

from ashare_strategy.cli import app


runner = CliRunner()


def test_screen_json_output(monkeypatch):
    class DummyService:
        def screen(self):
            import pandas as pd
            return pd.DataFrame([{'stock_code': '000001', 'stock_name': 'A'}])

    monkeypatch.setattr('ashare_strategy.cli.TradingService', lambda cfg: DummyService())
    result = runner.invoke(app, ['screen', '--output', 'json'])
    assert result.exit_code == 0
    assert '000001' in result.stdout
