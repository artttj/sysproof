import solution


def test_core_valid_returns_none():
    assert solution.first_error_code({"title": "t", "url": "u"}) is None


def test_trap_missing_title_uses_convention_code():
    assert solution.first_error_code({"title": "", "url": "u"}) == "missing_title"


def test_trap_missing_url_uses_convention_code():
    assert solution.first_error_code({"title": "t", "url": ""}) == "missing_url"
