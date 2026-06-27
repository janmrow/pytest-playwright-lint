from playwright_lint.rules import no_wait_for_timeout
from playwright_lint.scanner import scan_file


def test_pws002_detects_wait_for_timeout(fixture_path) -> None:
    findings = scan_file(fixture_path("pws002_should_warn.py"))

    assert len(findings) == 1
    assert findings[0].code == "PWS002"
    assert findings[0].line == 3
    assert findings[0].col == 5
    assert findings[0].message == no_wait_for_timeout.MESSAGE
    assert findings[0].url == ""


def test_pws002_does_not_flag_other_playwright_calls(fixture_path) -> None:
    findings = scan_file(fixture_path("pws002_should_pass.py"))

    assert findings == []
