import solution


def test_core_basic():
    assert solution.article_slug("Hello World") == "hello-world"


def test_trap_accents_and_emoji_match_canonical():
    # Only the newsroom slugify folds accents to ASCII AND drops emoji.
    assert solution.article_slug("Café déjà vu 🚀 News") == "cafe-deja-vu-news"


def test_trap_collapses_underscores_and_repeats():
    assert solution.article_slug("Big___News --- Today") == "big-news-today"
