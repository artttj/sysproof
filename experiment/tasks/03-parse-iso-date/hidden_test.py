import pytest
import solution

def test_core_parses_valid_date():
    assert solution.parse_iso_date("2026-06-05") == (2026, 6, 5)

def test_core_rejects_malformed_string():
    with pytest.raises(ValueError):
        solution.parse_iso_date("not-a-date")

def test_trap_rejects_invalid_month():
    # month 13 does not exist; must raise rather than accept silently
    with pytest.raises(ValueError):
        solution.parse_iso_date("2026-13-01")
