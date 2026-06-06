from harness.arms import arm_prefix, ARMS

def test_three_arms():
    assert ARMS == ["control", "placebo", "sysproof"]

def test_control_is_empty():
    assert arm_prefix("control", "SKILL TEXT") == ""

def test_placebo_is_one_line_no_structure():
    p = arm_prefix("placebo", "SKILL TEXT")
    assert "verify your work" in p.lower()
    assert "VERDICT" not in p  # placebo must not leak the gate structure

def test_sysproof_uses_skill_text():
    assert arm_prefix("sysproof", "SKILL TEXT") == "SKILL TEXT"

def test_unknown_arm_raises():
    import pytest
    with pytest.raises(ValueError):
        arm_prefix("bogus", "x")
