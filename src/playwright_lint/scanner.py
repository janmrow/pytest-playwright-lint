import ast
import os
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from pathlib import Path

from playwright_lint.finding import Finding
from playwright_lint.rules import (
    no_networkidle,
    no_time_sleep,
    no_wait_for_timeout,
)

DEFAULT_EXCLUDED_DIRS = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".tox",
        "build",
        "dist",
        "node_modules",
    }
)

RuleCheck = Callable[[ast.AST, Path], list[Finding]]

ALL_RULES: tuple[RuleCheck, ...] = (
    no_time_sleep.check,
    no_networkidle.check,
    no_wait_for_timeout.check,
)


@dataclass(frozen=True)
class ScanError:
    path: Path
    message: str


@dataclass(frozen=True)
class ScanResult:
    findings: tuple[Finding, ...]
    errors: tuple[ScanError, ...]


def discover_python_files(paths: Iterable[Path]) -> tuple[list[Path], list[ScanError]]:
    files: list[Path] = []
    errors: list[ScanError] = []

    for path in paths:
        if not path.exists():
            errors.append(ScanError(path=path, message="path does not exist"))
            continue

        if path.is_file():
            if path.suffix == ".py":
                files.append(path)
            continue

        if path.is_dir():
            files.extend(_discover_python_files_in_directory(path))
            continue

        errors.append(ScanError(path=path, message="unsupported path type"))

    return sorted(files, key=_sort_path), errors


def scan_file(path: Path, rules: Iterable[RuleCheck] = ALL_RULES) -> list[Finding]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))

    findings: list[Finding] = []
    for rule in rules:
        findings.extend(rule(tree, path))

    return sorted(findings, key=_sort_finding)


def scan_paths(paths: Iterable[Path]) -> ScanResult:
    files, errors = discover_python_files(paths)
    findings: list[Finding] = []

    for path in files:
        try:
            findings.extend(scan_file(path))
        except SyntaxError:
            errors.append(ScanError(path=path, message="cannot parse Python file"))
        except (OSError, UnicodeDecodeError):
            errors.append(ScanError(path=path, message="cannot read file"))

    return ScanResult(
        findings=tuple(sorted(findings, key=_sort_finding)),
        errors=tuple(sorted(errors, key=lambda error: _sort_path(error.path))),
    )


def _discover_python_files_in_directory(directory: Path) -> list[Path]:
    files: list[Path] = []

    for root, dirnames, filenames in os.walk(directory):
        dirnames[:] = [
            dirname for dirname in dirnames if dirname not in DEFAULT_EXCLUDED_DIRS
        ]

        root_path = Path(root)
        for filename in filenames:
            path = root_path / filename
            if path.suffix == ".py":
                files.append(path)

    return files


def _sort_finding(finding: Finding) -> tuple[str, int, int, str]:
    return (_sort_path(finding.path), finding.line, finding.col, finding.code)


def _sort_path(path: Path) -> str:
    return path.as_posix()
