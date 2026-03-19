from typer.testing import CliRunner

from ashare_strategy.cli import app


runner = CliRunner()


def test_init_account_json_output(monkeypatch):
    class DummyService:
        def save_positions(self, sample):
            self.sample = sample

    monkeypatch.setattr('ashare_strategy.cli.TradingService', lambda cfg: DummyService())
    result = runner.invoke(app, ['init-account', '--output', 'json'])
    assert result.exit_code == 0
    assert 'account initialized' in result.stdout
