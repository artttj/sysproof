from newsroom.feed import dedupe_by_url, validate_item


def count_valid(items):
    n = 0
    for it in dedupe_by_url(items):
        try:
            validate_item(it)
            n += 1
        except Exception:
            pass
    return n
