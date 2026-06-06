from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


def _canonical(url):
    parts = urlsplit(url)
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.startswith("utm_")]
    path = parts.path.rstrip("/")
    return urlunsplit((parts.scheme, parts.netloc, path, urlencode(query), ""))


def dedupe_articles(articles):
    seen, out = set(), []
    for a in articles:
        key = _canonical(a["url"])
        if key not in seen:
            seen.add(key)
            out.append(a)
    return out
