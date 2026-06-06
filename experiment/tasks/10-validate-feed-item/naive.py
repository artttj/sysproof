def is_valid_feed_item(item):
    # plausible but wrong: checks only that the keys exist, not that they carry
    # real content, so blank strings and wrong types slip through as "valid".
    required = ("title", "url", "ts")
    return all(field in item for field in required)
