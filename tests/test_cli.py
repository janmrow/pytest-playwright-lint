from click.testing import CliRunner

from playwright_lint.cli import main


def test_cli_runs_bootstrap_command() -> None:
    runner = CliRunner()

    result = runner.invoke(main)

    assert result.exit_code == 0
    assert "pytest-playwright-lint is installed" in result.output
    assert "Scanning will be added in M01" in result.output


def test_cli_version_option() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert "playwright-lint, version" in result.output
