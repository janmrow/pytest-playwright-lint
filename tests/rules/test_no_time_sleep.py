from playwright_lint.rules import no_time_sleep
from playwright_lint.scanner import scan_file


def test_pws001_detects_time_sleep(fixture_path) -> None:
    findings = scan_file(fixture_path("pws001_should_warn.py"))

    assert len(findings) == 1
    assert findings[0].code == "PWS001"
    assert findings[0].line == 6
    assert findings[0].col == 5
    assert findings[0].message == no_time_sleep.MESSAGE
    assert findings[0].url == ""


def test_pws001_does_not_flag_unqualified_sleep(fixture_path) -> None:
    findings = scan_file(fixture_path("pws001_should_pass.py"))

    assert findings == []
