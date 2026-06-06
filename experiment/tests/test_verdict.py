from harness.verdict import parse_verdict

def test_done_uppercase():
    assert parse_verdict("work done\nVERDICT: DONE") == "DONE"

def test_not_done():
    assert parse_verdict("VERDICT: NOT_DONE") == "NOT_DONE"

def test_case_insensitive_and_trailing():
    assert parse_verdict("verdict: done  ") == "DONE"

def test_last_verdict_wins():
    assert parse_verdict("VERDICT: NOT_DONE\n...\nVERDICT: DONE") == "DONE"

def test_missing_returns_none():
    assert parse_verdict("I finished the task.") is None
