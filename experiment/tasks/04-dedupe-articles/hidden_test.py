import solution

def test_core_removes_exact_duplicate_urls():
    arts = [
        {"url": "https://news.example/a"},
        {"url": "https://news.example/b"},
        {"url": "https://news.example/a"},
    ]
    out = solution.dedupe_articles(arts)
    assert [a["url"] for a in out] == ["https://news.example/a", "https://news.example/b"]

def test_core_keeps_distinct_articles():
    arts = [{"url": "https://news.example/a"}, {"url": "https://news.example/c"}]
    assert len(solution.dedupe_articles(arts)) == 2

def test_trap_same_story_with_slash_and_utm():
    arts = [
        {"url": "https://news.example/story"},
        {"url": "https://news.example/story/"},
        {"url": "https://news.example/story?utm_source=tw"},
    ]
    out = solution.dedupe_articles(arts)
    assert len(out) == 1
    assert out[0]["url"] == "https://news.example/story"
