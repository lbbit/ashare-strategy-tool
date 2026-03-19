from typer.testing import CliRunner

from ashare_strategy.cli import app


runner = CliRunner()


def test_positions_json_output(monkeypatch):
    class DummyService:
        def load_account(self):
            return {'cash': 10000, 'positions': [{'stock_code': '000001'}]}

    monkeypatch.setattr('ashare_strategy.cli.TradingService', lambda cfg: DummyService())
    result = runner.invoke(app, ['positions', '--output', 'json'])
    assert result.exit_code == 0
    assert 'success' in result.stdout
    assert '000001' in result.stdout
