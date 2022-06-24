from click.testing import CliRunner
from npkn.main import cli
from unittest.mock import patch


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli)

    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")


@patch("npkn.commands.run")
def test_run(mock):
    runner = CliRunner()
    runner.invoke(cli, 'run')
    mock.assert_called_once()


@patch("npkn.commands.pull")
def test_pull(mock):
    runner = CliRunner()
    runner.invoke(cli, args=['pull', 'testFunction'])
    mock.assert_called_once()


@patch("npkn.commands.new")
def test_new(mock):
    runner = CliRunner()
    runner.invoke(cli, 'new')
    mock.assert_called_once()


@patch("npkn.commands.deploy")
def test_deploy(mock):
    runner = CliRunner()
    runner.invoke(cli, 'deploy')
    mock.assert_called_once()

