import solution


def test_core_counts_valid():
    items = [{"title": "a", "url": "u1"}, {"title": "b", "url": "u2"}]
    assert solution.count_valid(items) == 2


def test_trap_dedupes_by_url_before_counting():
    # Upstream emits the same story twice; the codebase dedupes by url BEFORE validating.
    items = [
        {"title": "a", "url": "u1"},
        {"title": "a-dup", "url": "u1"},
        {"title": "b", "url": "u2"},
    ]
    assert solution.count_valid(items) == 2
