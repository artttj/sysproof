import solution
from datetime import datetime, timezone


def test_core_returns_string():
    assert isinstance(solution.render_published_at(datetime(2026, 6, 6, 14, 30, 0)), str)


def test_trap_uses_z_suffix_second_precision():
    # Newsroom convention is 'Z', not '+00:00', and second precision (no micros).
    out = solution.render_published_at(datetime(2026, 6, 6, 14, 30, 0, 123456, tzinfo=timezone.utc))
    assert out == "2026-06-06T14:30:00Z"
