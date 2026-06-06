def count_valid(items):
    return sum(1 for it in items if it.get("title") and it.get("url"))
