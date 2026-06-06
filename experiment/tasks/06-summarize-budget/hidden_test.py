import solution

def test_core_short_text_unchanged():
    assert solution.fit_to_budget("Short update", 280) == "Short update"

def test_core_does_not_cut_mid_word():
    text = "alpha beta gamma delta epsilon"
    out = solution.fit_to_budget(text, 12)
    assert len(out) <= 12
    # must end on a complete word
    assert out in ("alpha beta", "alpha")
    assert not out.endswith("gam")

def test_trap_budget_is_characters_not_words():
    # 40 words of 9 chars each = ~400 chars, well under any word-count reading of
    # 280 but far over a 280-CHARACTER budget. A word-count interpretation fails.
    text = " ".join(["wednesday"] * 40)
    out = solution.fit_to_budget(text, 280)
    assert len(out) <= 280
