import re


def slugify(title):
    # plausible but wrong: lowercases and hyphenates, but never folds accents to
    # ASCII. Python's \w matches unicode letters, so "café" keeps its "é" and
    # other non-ASCII letters survive into the slug.
    lowered = title.lower()
    slug = re.sub(r"[^\w]+", "-", lowered, flags=re.UNICODE)
    return slug.strip("-")
