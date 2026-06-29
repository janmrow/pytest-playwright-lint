from textwrap import dedent

from click.testing import CliRunner

from playwright_lint.cli import main
from playwright_lint.exit_codes import EXIT_ERROR, EXIT_FINDINGS, EXIT_OK


def test_cli_reports_no_findings_for_clean_file() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("test_ok.py", "w", encoding="utf-8") as file:
            file.write("def test_ok(page):\n    page.goto('/login')\n")

        result = runner.invoke(main, ["test_ok.py"])

    assert result.exit_code == EXIT_OK
    assert result.output == "No findings.\n"


def test_cli_reports_pws001_finding() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("test_bad.py", "w", encoding="utf-8") as file:
            file.write(
                dedent(
                    """
                    import time


                    def test_login(page):
                        time.sleep(3)
                    """
                ).lstrip()
            )

        result = runner.invoke(main, ["test_bad.py"])

    assert result.exit_code == EXIT_FINDINGS
    assert (
        "test_bad.py:5:5 PWS001 Avoid time.sleep() in Playwright tests; prefer "
        "a locator assertion or a specific wait condition.\n"
    ) == result.output


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


def test_cli_returns_error_for_missing_path() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(main, ["missing.py"])

    assert result.exit_code == EXIT_ERROR
    assert "missing.py: path does not exist\n" in _error_output(result)


def test_cli_returns_error_when_parse_error_exists_even_with_findings() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("bad.py", "w", encoding="utf-8") as file:
            file.write("def broken(:\n")

        with open("test_bad.py", "w", encoding="utf-8") as file:
            file.write("def test_login(page):\n    page.wait_for_timeout(3000)\n")

        result = runner.invoke(main, ["bad.py", "test_bad.py"])

    assert result.exit_code == EXIT_ERROR
    assert "bad.py: cannot parse Python file\n" in _error_output(result)
    assert "test_bad.py:2:5 PWS002" in result.output


def test_cli_ignores_non_python_file() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        with open("README.md", "w", encoding="utf-8") as file:
            file.write("page.wait_for_timeout(3000)\n")

        result = runner.invoke(main, ["README.md"])

    assert result.exit_code == EXIT_OK
    assert result.output == "No findings.\n"


def test_cli_version_option() -> None:
    runner = CliRunner()

    result = runner.invoke(main, ["--version"])

    assert result.exit_code == 0
    assert "playwright-lint, version" in result.output


def _error_output(result) -> str:
    return getattr(result, "stderr", "") or result.output
