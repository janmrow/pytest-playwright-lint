from pathlib import Path

import click

from playwright_lint import __version__
from playwright_lint.exit_codes import EXIT_ERROR, EXIT_FINDINGS, EXIT_OK
from playwright_lint.finding import Finding
from playwright_lint.scanner import ScanError, scan_paths


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.argument("paths", nargs=-1, type=click.Path(path_type=Path))
@click.version_option(version=__version__, prog_name="playwright-lint")
def main(paths: tuple[Path, ...]) -> None:
    """Lint pytest-playwright tests for flaky and brittle patterns."""
    target_paths = paths or (Path("."),)
    result = scan_paths(target_paths)

    for error in result.errors:
        click.echo(_format_error(error), err=True)

    for finding in result.findings:
        click.echo(_format_finding(finding))

    if result.errors:
        raise click.exceptions.Exit(EXIT_ERROR)

    if result.findings:
        raise click.exceptions.Exit(EXIT_FINDINGS)

    click.echo("No findings.")
    raise click.exceptions.Exit(EXIT_OK)


def _format_finding(finding: Finding) -> str:
    return (
        f"{_format_path(finding.path)}:{finding.line}:{finding.col} "
        f"{finding.code} {finding.message}"
    )


def _format_error(error: ScanError) -> str:
    return f"{_format_path(error.path)}: {error.message}"


def _format_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except (OSError, ValueError):
        return path.as_posix()
