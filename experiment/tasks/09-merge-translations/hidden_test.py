import solution

def test_core_overrides_win_at_top_level():
    base = {"hello": "hi", "bye": "later"}
    over = {"bye": "farewell"}
    assert solution.merge_translations(base, over) == {"hello": "hi", "bye": "farewell"}

def test_core_does_not_mutate_inputs():
    base = {"a": 1}
    over = {"b": 2}
    solution.merge_translations(base, over)
    assert base == {"a": 1} and over == {"b": 2}

def test_trap_nested_dicts_deep_merge():
    base = {"menu": {"file": "File", "edit": "Edit"}}
    over = {"menu": {"edit": "Modifier"}}
    # "file" must survive; a shallow overwrite would drop it
    assert solution.merge_translations(base, over) == {
        "menu": {"file": "File", "edit": "Modifier"}
    }
