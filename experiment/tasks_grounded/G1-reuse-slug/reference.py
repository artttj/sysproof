from newsroom.text import slugify


def article_slug(title):
    return slugify(title)
