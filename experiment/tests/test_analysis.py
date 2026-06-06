import math
from analysis import wilson_ci, arr_rrr, fisher_holm, false_done_rate_by_arm
from harness.results import Row

def test_wilson_ci_known_values():
    lo, hi = wilson_ci(5, 100)  # 5%
    assert 0.02 < lo < 0.05 < hi < 0.12

def test_wilson_ci_zero_events():
    lo, hi = wilson_ci(0, 50)
    assert lo == 0.0
    assert 0 < hi < 0.1

def test_arr_rrr():
    arr, rrr = arr_rrr(p_control=0.40, p_treat=0.10)
    assert abs(arr - 0.30) < 1e-9
    assert abs(rrr - 0.75) < 1e-9

def test_fisher_holm_two_comparisons():
    # sysproof much lower than both control and placebo
    res = fisher_holm(
        treat=("sysproof", 2, 100),       # 2 false-done of 100
        comparators=[("control", 40, 100), ("placebo", 30, 100)],
    )
    assert res["control"]["p_holm"] < 0.05
    assert res["placebo"]["p_holm"] < 0.05

def test_rate_by_arm_counts():
    rows = [
        Row("t1", "control", 0, True, False, False, "DONE"),   # false-done
        Row("t1", "control", 1, True, True, True, "DONE"),     # not false-done
        Row("t1", "sysproof", 0, False, False, True, "NOT_DONE"),  # not false-done
    ]
    by = false_done_rate_by_arm(rows)
    assert by["control"]["events"] == 1 and by["control"]["n"] == 2
    assert by["sysproof"]["events"] == 0 and by["sysproof"]["n"] == 1
