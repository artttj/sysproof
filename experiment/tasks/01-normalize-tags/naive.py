def normalize_tags(tags):
    # plausible but wrong: dedupes BEFORE lowercasing, so "World"/"world" survive
    out = []
    for t in tags:
        if t not in out:
            out.append(t)
    return [t.lower() for t in out]
