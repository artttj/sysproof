import solution

def test_core_basic_words():
    assert solution.slugify("Hello World") == "hello-world"

def test_core_collapses_punctuation_and_spaces():
    assert solution.slugify("Breaking:   Big   News!!!") == "breaking-big-news"

def test_trap_strips_accents_and_emoji():
    # accented letters must fold to ASCII; emoji must be removed entirely
    assert solution.slugify("Café déjà vu 🚀 News") == "cafe-deja-vu-news"
