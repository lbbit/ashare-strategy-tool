from typer.testing import CliRunner

from ashare_strategy.cli import app


runner = CliRunner()


def test_version_command_text():
    result = runner.invoke(app, ['version'])
    assert result.exit_code == 0
    assert 'ashare-strategy-tool' in result.stdout
