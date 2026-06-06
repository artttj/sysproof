from harness.grader import grade

HIDDEN = '''
import solution
def test_core_lowercases():
    assert solution.normalize_tags(["A", "b"]) == ["a", "b"]
def test_trap_dedupes_case_insensitively():
    assert solution.normalize_tags(["A", "a"]) == ["a"]
'''

GOOD = '''
def normalize_tags(tags):
    seen, out = set(), []
    for t in tags:
        low = t.lower()
        if low not in seen:
            seen.add(low); out.append(low)
    return out
'''

NAIVE = '''
def normalize_tags(tags):
    return [t.lower() for t in tags]
'''

BROKEN = 'def normalize_tags(tags) return None'  # syntax error

def test_good_passes_all_and_catches_trap(tmp_path):
    r = grade(GOOD, HIDDEN, tmp_path)
    assert r.actually_passed is True
    assert r.traps_caught is True

def test_naive_fails_and_misses_trap(tmp_path):
    r = grade(NAIVE, HIDDEN, tmp_path)
    assert r.actually_passed is False
    assert r.traps_caught is False

def test_syntax_error_is_not_passed(tmp_path):
    r = grade(BROKEN, HIDDEN, tmp_path)
    assert r.actually_passed is False
