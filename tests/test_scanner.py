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


def test_discovery_reports_missing_path(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.py"

    files, errors = discover_python_files([missing_path])

    assert files == []
    assert len(errors) == 1
    assert errors[0].path == missing_path
    assert errors[0].message == "path does not exist"


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


def test_direct_python_file_inside_excluded_directory_can_be_scanned(
    tmp_path: Path,
) -> None:
    direct_file = tmp_path / ".venv" / "test_bad.py"
    direct_file.parent.mkdir()
    direct_file.write_text(
        "def test_login(page):\n    page.wait_for_timeout(3000)\n",
        encoding="utf-8",
    )

    result = scan_paths([direct_file])

    assert result.errors == ()
    assert len(result.findings) == 1
    assert result.findings[0].path == direct_file


def test_scan_paths_reports_parse_error_and_continues(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad.py"
    good_file = tmp_path / "good.py"
    bad_file.write_text("def broken(:\n", encoding="utf-8")
    good_file.write_text(
        "def test_login(page):\n    page.wait_for_timeout(3000)\n",
        encoding="utf-8",
    )

    result = scan_paths([bad_file, good_file])

    assert len(result.errors) == 1
    assert result.errors[0].path == bad_file
    assert result.errors[0].message == "cannot parse Python file"
    assert len(result.findings) == 1
    assert result.findings[0].path == good_file
    assert result.findings[0].code == "PWS002"


def test_scan_paths_reports_encoding_error_and_continues(tmp_path: Path) -> None:
    bad_file = tmp_path / "bad_encoding.py"
    good_file = tmp_path / "good.py"
    bad_file.write_bytes(b"\xff\xfe\xfa")
    good_file.write_text(
        "def test_login(page):\n    page.wait_for_timeout(3000)\n",
        encoding="utf-8",
    )

    result = scan_paths([bad_file, good_file])

    assert len(result.errors) == 1
    assert result.errors[0].path == bad_file
    assert result.errors[0].message == "cannot read file"
    assert len(result.findings) == 1
    assert result.findings[0].path == good_file
    assert result.findings[0].code == "PWS002"


def test_scan_paths_sorts_findings_deterministically(tmp_path: Path) -> None:
    later_file = tmp_path / "b_later.py"
    earlier_file = tmp_path / "a_earlier.py"

    later_file.write_text(
        "\n\ndef test_later(page):\n    page.wait_for_timeout(3000)\n",
        encoding="utf-8",
    )
    earlier_file.write_text(
        "def test_earlier(page):\n    page.wait_for_timeout(3000)\n",
        encoding="utf-8",
    )

    result = scan_paths([later_file, earlier_file])

    assert result.errors == ()
    assert [finding.path for finding in result.findings] == [
        earlier_file,
        later_file,
    ]
    assert [finding.line for finding in result.findings] == [2, 4]


def test_scan_paths_sorts_errors_deterministically(tmp_path: Path) -> None:
    later_file = tmp_path / "z_bad.py"
    earlier_file = tmp_path / "a_bad.py"

    later_file.write_text("def broken(:\n", encoding="utf-8")
    earlier_file.write_text("def broken(:\n", encoding="utf-8")

    result = scan_paths([later_file, earlier_file])

    assert result.findings == ()
    assert [error.path for error in result.errors] == [
        earlier_file,
        later_file,
    ]
