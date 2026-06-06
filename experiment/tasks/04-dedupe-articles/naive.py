def dedupe_articles(articles):
    # plausible but wrong: dedupes on the raw url string, so the same story with
    # a trailing slash or utm_* params survives as a "different" article.
    seen, out = set(), []
    for a in articles:
        url = a["url"]
        if url not in seen:
            seen.add(url)
            out.append(a)
    return out
