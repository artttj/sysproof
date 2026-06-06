import re


def article_slug(title):
    return re.sub(r"\s+", "-", title.strip().lower())
