from typer.testing import CliRunner

from ashare_strategy.cli import app


runner = CliRunner()


def test_plan_json_output(monkeypatch):
    class DummyPlannerService:
        def export_daily_plan(self, output_dir='daily_plan'):
            return {'output_dir': output_dir, 'plan': {'summary': {'candidate_count': 1}, 'buy_candidates': [], 'hold_positions': [], 'sell_review': []}}

    class DummyTradingService:
        pass

    monkeypatch.setattr('ashare_strategy.cli.TradingService', lambda cfg: DummyTradingService())
    monkeypatch.setattr('ashare_strategy.cli.TradingPlanner', lambda service, cfg: DummyPlannerService())
    result = runner.invoke(app, ['plan', '--output', 'json'])
    assert result.exit_code == 0
    assert 'candidate_count' in result.stdout
