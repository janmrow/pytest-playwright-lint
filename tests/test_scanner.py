from pathlib import Path

from playwright_lint.scanner import discover_python_files, scan_paths


def test_scan_paths_detects_pws002_in_python_file(tmp_path: Path) -> None:
    test_file = tmp_path / "test_login.py"
    test_file.write_text(
        "def test_login(page):\n    page.wait_for_timeout(3000)\n",
        encoding="utf-8",
    )

    result = scan_paths([test_file])

    assert result.errors == ()
    assert len(result.findings) == 1
    assert result.findings[0].code == "PWS002"


def test_discovery_ignores_non_python_files(tmp_path: Path) -> None:
    readme = tmp_path / "README.md"
    readme.write_text("page.wait_for_timeout(3000)\n", encoding="utf-8")

    files, errors = discover_python_files([readme])

    assert files == []
    assert errors == []


def test_discovery_skips_default_excluded_directories(tmp_path: Path) -> None:
    excluded_file = tmp_path / ".venv" / "test_bad.py"
    included_file = tmp_path / "tests" / "test_good.py"
    excluded_file.parent.mkdir()
    included_file.parent.mkdir()
    excluded_file.write_text("page.wait_for_timeout(3000)\n", encoding="utf-8")
    included_file.write_text("def test_ok():\n    pass\n", encoding="utf-8")

    files, errors = discover_python_files([tmp_path])

    assert errors == []
    assert files == [included_file]
