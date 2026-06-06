import re
import unicodedata

_PUNCT = re.compile(r"[^\w\s-]", re.UNICODE)
_SPACES = re.compile(r"[\s_-]+")


def slugify(value):
    """Canonical newsroom slug: NFKD-fold accents to ASCII, drop emoji/punctuation,
    collapse whitespace/underscores/hyphens to a single '-', lowercase, strip ends."""
    norm = unicodedata.normalize("NFKD", value)
    ascii_only = norm.encode("ascii", "ignore").decode("ascii")
    cleaned = _PUNCT.sub("", ascii_only).strip().lower()
    return _SPACES.sub("-", cleaned).strip("-")
