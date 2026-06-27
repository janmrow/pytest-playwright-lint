from pathlib import Path

import pytest


@pytest.fixture
def fixture_path():
    base = Path(__file__).parent / "fixtures"
    return lambda name: base / name
