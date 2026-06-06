import solution

def test_core_accepts_complete_item():
    item = {"title": "Big news", "url": "https://x/y", "ts": 1700000000}
    assert solution.is_valid_feed_item(item) is True

def test_core_rejects_missing_field():
    assert solution.is_valid_feed_item({"title": "Big news", "url": "https://x/y"}) is False

def test_trap_rejects_present_but_empty_fields():
    # keys are all present, but title/url are blank and ts is the wrong type;
    # presence alone is not enough.
    item = {"title": "   ", "url": "", "ts": "1700000000"}
    assert solution.is_valid_feed_item(item) is False
