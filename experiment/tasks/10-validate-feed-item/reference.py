def is_valid_feed_item(item):
    if not isinstance(item, dict):
        return False
    required = ("title", "url", "ts")
    if any(field not in item for field in required):
        return False
    title, url, ts = item["title"], item["url"], item["ts"]
    if not isinstance(title, str) or not title.strip():
        return False
    if not isinstance(url, str) or not url.strip():
        return False
    if not isinstance(ts, int) or isinstance(ts, bool):
        return False
    return True
