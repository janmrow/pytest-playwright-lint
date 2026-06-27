# pytest-playwright-lint

A small Python quality gate for `pytest-playwright` tests.

It detects common patterns that make browser tests slower, flakier, or harder to maintain.

## Status

Early development.

Current milestone:

```text
M00 — Bootstrap repo
```

The scanner and rules will be added incrementally.

## Goals

`pytest-playwright-lint` is intended to be:

- small,
- clear,
- tested,
- boring,
- useful,
- educational,
- CI-friendly.

## Non-goals for v0.1

This project does not aim to be a full Python equivalent of ESLint for Playwright.

Not included in v0.1:

- type-aware analysis,
- autofixes,
- JSON output,
- rule configuration,
- PyPI publishing,
- IDE integration,
- Ruff plugin integration.

## Development setup

```bash
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Local checks

```bash
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

## CLI

At this bootstrap stage, the command only verifies that the package is installed:

```bash
playwright-lint
playwright-lint --version
```

Scanning will be added in M01.
