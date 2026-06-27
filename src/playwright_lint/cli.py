import click

from playwright_lint import __version__


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="playwright-lint")
def main() -> None:
    """Lint pytest-playwright tests for flaky and brittle patterns."""
    click.echo("pytest-playwright-lint is installed. Scanning will be added in M01.")
