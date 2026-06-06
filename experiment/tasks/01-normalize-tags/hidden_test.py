import solution

def test_core_lowercases_and_orders():
    assert solution.normalize_tags(["World", "Tech"]) == ["world", "tech"]

def test_core_removes_exact_duplicates():
    assert solution.normalize_tags(["a", "b", "a"]) == ["a", "b"]

def test_trap_dedupes_case_insensitively():
    # "World" and "world" are the same tag once lowercased
    assert solution.normalize_tags(["World", "world", "WORLD"]) == ["world"]
