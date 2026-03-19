from typer.testing import CliRunner
from unittest.mock import patch

from ashare_strategy.cli import app


runner = CliRunner()


def test_screen_failure_returns_friendly_error():
    with patch('ashare_strategy.cli.TradingService') as service_cls, patch('ashare_strategy.cli.build_provider_diagnostics', return_value={'provider': 'akshare', 'status': 'error'}), patch('ashare_strategy.cli.format_provider_hint', return_value='hint'):
        service_cls.return_value.screen.side_effect = RuntimeError('boom')
        result = runner.invoke(app, ['screen'])
        assert result.exit_code == 1
        assert '选股失败' in result.stdout
