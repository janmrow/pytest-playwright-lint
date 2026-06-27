from textwrap import dedent

from click.testing import CliRunner

from playwright_lint.cli import main
from playwright_lint.exit_codes import EXIT_FINDINGS, EXIT_OK


def test_cli_reports_no_findings_for_clean_file() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("test_ok.py", "w", encoding="utf-8") as file:
            file.write("def test_ok(page):\n    page.goto('/login')\n")

        result = runner.invoke(main, ["test_ok.py"])

    assert result.exit_code == EXIT_OK
    assert result.output == "No findings.\n"


def test_cli_reports_pws002_finding() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("test_bad.py", "w", encoding="utf-8") as file:
            file.write(
                dedent(
                    """
                    def test_login(page):
                        page.wait_for_timeout(3000)
                    """
                ).lstrip()
            )

        result = runner.invoke(main, ["test_bad.py"])

    assert result.exit_code == EXIT_FINDINGS
    assert (
        "test_bad.py:2:5 PWS002 Avoid page.wait_for_timeout(); prefer a locator "
        "assertion or a specific wait condition.\n"
    ) == result.output


def test_cli_defaults_to_current_directory() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("test_bad.py", "w", encoding="utf-8") as file:
            file.write("def test_login(page):\n    page.wait_for_timeout(3000)\n")

        result = runner.invoke(main)

    assert result.exit_code == EXIT_FINDINGS
    assert "test_bad.py:2:5 PWS002" in result.output


def test_cli_version_option() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert "playwright-lint, version" in result.output
