import solution

def test_core_sorts_newest_first():
    arts = [{"id": "a", "ts": 10}, {"id": "b", "ts": 30}, {"id": "c", "ts": 20}]
    assert [x["id"] for x in solution.rank_by_recency(arts)] == ["b", "c", "a"]

def test_core_preserves_tie_order():
    arts = [{"id": "a", "ts": 5}, {"id": "b", "ts": 5}, {"id": "c", "ts": 9}]
    assert [x["id"] for x in solution.rank_by_recency(arts)] == ["c", "a", "b"]

def test_trap_missing_timestamps_sort_last():
    # articles without a usable timestamp must land at the END, not the front
    arts = [
        {"id": "a", "ts": None},
        {"id": "b", "ts": 50},
        {"id": "c"},
        {"id": "d", "ts": 10},
    ]
    assert [x["id"] for x in solution.rank_by_recency(arts)] == ["b", "d", "a", "c"]
