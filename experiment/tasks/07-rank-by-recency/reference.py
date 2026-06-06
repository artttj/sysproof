def rank_by_recency(articles):
    def key(item):
        idx, art = item
        ts = art.get("ts")
        has_ts = ts is not None
        # newest first among those with a ts; missing ts sorts last; ties keep
        # original order via the enumeration index.
        return (0 if has_ts else 1, -ts if has_ts else 0, idx)

    indexed = list(enumerate(articles))
    indexed.sort(key=key)
    return [art for _, art in indexed]
