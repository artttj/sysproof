from .errors import FeedError


def dedupe_by_url(items):
    """Items must be deduped by url BEFORE validation - the upstream fetcher emits
    the same story from multiple sources, and validating dupes double-counts them.
    Keeps first occurrence, preserves order."""
    seen = set()
    out = []
    for it in items:
        url = it.get("url")
        if url in seen:
            continue
        seen.add(url)
        out.append(it)
    return out


def validate_item(item):
    """Raises FeedError if invalid. Assumes input is ALREADY deduped (see dedupe_by_url)."""
    if not item.get("title"):
        raise FeedError("missing_title", "feed item has no title")
    if not item.get("url"):
        raise FeedError("missing_url", "feed item has no url")
    return True
