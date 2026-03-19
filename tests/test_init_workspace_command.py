from typer.testing import CliRunner

from ashare_strategy.cli import app


runner = CliRunner()


def test_init_workspace_json_output(monkeypatch, tmp_path):
    class DummyService:
        def save_positions(self, sample):
            self.sample = sample

    monkeypatch.setattr('ashare_strategy.cli.TradingService', lambda cfg: DummyService())
    result = runner.invoke(app, ['init-workspace', '--output-dir', str(tmp_path / 'workspace'), '--output', 'json'])
    assert result.exit_code == 0
    assert 'workspace initialized' in result.stdout
    assert 'positions_initialized' in result.stdout
