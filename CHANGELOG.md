# Changelog

## 0.1.0 — Unreleased

Initial local MVP in progress.

Added so far:

- Bootstrap Python package structure.
- Add Click-based `playwright-lint` CLI.
- Add recursive Python file discovery.
- Add deterministic `Finding` model.
- Add exit code constants.
- Add first AST rule: `PWS002` for `page.wait_for_timeout()`.
- Add text reporting for findings.
- Add CLI, scanner, and rule tests.
- Test scanner behavior for missing paths, non-Python files, default exclusions, parse errors, read errors, and deterministic ordering.
- Test CLI error precedence when parse/read/input errors occur.

Planned v0.1 scope:

- local CLI,
- recursive Python file scanning,
- six deterministic AST-based rules,
- text report,
- stable exit codes,
- pytest test coverage,
- basic README,
- local pre-commit usage,
- GitHub Actions CI.
