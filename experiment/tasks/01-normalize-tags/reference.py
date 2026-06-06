def normalize_tags(tags):
    seen, out = set(), []
    for t in tags:
        low = t.lower()
        if low not in seen:
            seen.add(low)
            out.append(low)
    return out
