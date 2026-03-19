from typer.testing import CliRunner

from ashare_strategy.cli import app


runner = CliRunner()


def test_init_workspace_creates_directories(monkeypatch, tmp_path):
    class DummyService:
        def save_positions(self, sample):
            self.sample = sample

    monkeypatch.setattr('ashare_strategy.cli.TradingService', lambda cfg: DummyService())
    result = runner.invoke(app, ['init-workspace', '--output-dir', str(tmp_path / 'workspace'), '--output', 'json'])
    assert result.exit_code == 0
    assert 'directories' in result.stdout
    assert (tmp_path / 'workspace' / 'reports').exists()
    assert (tmp_path / 'workspace' / 'daily_plan').exists()
