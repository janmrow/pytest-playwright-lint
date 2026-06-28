# pytest-playwright-lint

A small Python quality gate for `pytest-playwright` tests.

It detects common patterns that make browser tests slower, flakier, or harder to maintain.

## Status

Early development.

Current milestone:

```text
M02 — Scanner behavior and errors
```

The first implemented rule is:

```text
PWS002 Avoid page.wait_for_timeout(); prefer a locator assertion or a specific wait condition.
```

## Why this exists

Browser tests can look correct while still containing patterns that make them slower or flaky.

This project focuses on small, deterministic AST-based checks for `pytest-playwright` test code.

It does not write tests for you. It acts as a local quality gate.

## Example

Problematic test:

```python
def test_login(page):
    page.goto("/login")
    page.wait_for_timeout(3000)
```

Run:

```bash
playwright-lint tests/
```

Output:

```text
tests/test_login.py:3:5 PWS002 Avoid page.wait_for_timeout(); prefer a locator assertion or a specific wait condition.
```

Prefer waiting for a specific condition or using a locator assertion instead of waiting for a fixed timeout.

For example:

```python
from playwright.sync_api import expect


def test_login(page):
    page.goto("/login")
    expect(page.get_by_role("button", name="Sign in")).to_be_visible()
```

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

Scan one file:

```bash
playwright-lint tests/fixtures/pws002_should_pass.py
```

Scan a directory recursively:

```bash
playwright-lint tests/
```

Scan the current directory:

```bash
playwright-lint
```

Show the installed version:

```bash
playwright-lint --version
```

Scanner behavior in v0.1:

- no path means scan the current directory;
- directories are scanned recursively;
- files without `.py` are ignored without error;
- `.py` files are read as UTF-8;
- parse/read errors are reported without stopping the whole scan;
- default technical directories are skipped during recursive directory scans.

## Exit codes

```text
0 = no findings
1 = findings found
2 = invalid usage / parse error / read error / internal error
```

If at least one file cannot be parsed or read, the final exit code is `2`.
This also wins over findings, because the scan result is incomplete.

## Implemented rules

### PWS002 — `page.wait_for_timeout()`

Detects:

```python
page.wait_for_timeout(3000)
```

Message:

```text
PWS002 Avoid page.wait_for_timeout(); prefer a locator assertion or a specific wait condition.
```

Rationale:

- fixed timeouts wait for time, not for application state;
- they often make tests slower;
- they can hide missing synchronization;
- they can increase flaky behavior.
