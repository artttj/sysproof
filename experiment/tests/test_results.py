from harness.results import Row, write_rows, read_rows, false_done

def test_false_done_logic():
    assert false_done(claimed_done=True, actually_passed=False) is True
    assert false_done(claimed_done=True, actually_passed=True) is False
    assert false_done(claimed_done=False, actually_passed=False) is False

def test_roundtrip(tmp_path):
    rows = [
        Row("t1", "control", 0, True, False, False, "DONE"),
        Row("t1", "sysproof", 0, False, False, True, "NOT_DONE"),
    ]
    p = tmp_path / "results.csv"
    write_rows(rows, p)
    back = read_rows(p)
    assert back[0].task == "t1" and back[0].claimed_done is True
    assert back[1].arm == "sysproof" and back[1].traps_caught is True
