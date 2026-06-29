from pathlib import Path

from playwright_lint.rules import no_networkidle
from playwright_lint.scanner import scan_file


def test_pws003_detects_networkidle_load_state(fixture_path) -> None:
    findings = scan_file(fixture_path("pws003_should_warn.py"))

    assert len(findings) == 1
    assert findings[0].code == "PWS003"
    assert findings[0].line == 3
    assert findings[0].col == 5
    assert findings[0].message == no_networkidle.MESSAGE
    assert findings[0].url == ""


def test_pws003_detects_networkidle_state_keyword(tmp_path: Path) -> None:
    test_file = tmp_path / "test_dashboard.py"
    test_file.write_text(
        'def test_dashboard(page):\n    page.wait_for_load_state(state="networkidle")\n',
        encoding="utf-8",
    )

    findings = scan_file(test_file)

    assert len(findings) == 1
    assert findings[0].code == "PWS003"
    assert findings[0].line == 2
    assert findings[0].col == 5


def test_pws003_does_not_flag_other_load_states(fixture_path) -> None:
    findings = scan_file(fixture_path("pws003_should_pass.py"))

    assert findings == []
