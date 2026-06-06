from newsroom.errors import FeedError


def require_field(item, field):
    if not item.get(field):
        raise FeedError("missing_field", f"feed item has no {field}")
    return True
