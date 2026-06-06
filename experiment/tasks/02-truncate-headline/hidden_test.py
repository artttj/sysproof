import solution

def test_core_short_text_unchanged():
    assert solution.truncate_headline("Quick news", 50) == "Quick news"

def test_core_truncates_on_word_boundary():
    out = solution.truncate_headline("Markets rally as inflation cools sharply today", 20)
    assert len(out) <= 20
    assert out.endswith("…")
    # cuts at a word boundary, not mid-word
    assert out == "Markets rally as…"

def test_trap_long_single_word_is_hard_cut():
    # one word longer than the limit must still be forced to fit, not returned whole
    out = solution.truncate_headline("Supercalifragilisticexpialidocious", 10)
    assert len(out) <= 10
    assert out.endswith("…")
