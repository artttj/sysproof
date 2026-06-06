from newsroom.feed import validate_item
from newsroom.errors import FeedError


def first_error_code(item):
    """Return the first validation error code for a feed item, or None if valid.

    Delegates to newsroom.feed.validate_item which raises FeedError with a short
    code string for each problem. Returns that code, or None on success.
    """
    try:
        validate_item(item)
        return None
    except FeedError as exc:
        return exc.code
