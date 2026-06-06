import re

_VERDICT_RE = re.compile(r"VERDICT:\s*(DONE|NOT_DONE)", re.IGNORECASE)


def parse_verdict(text: str) -> str | None:
    """Return the LAST verdict found in text, or None if absent."""
    matches = _VERDICT_RE.findall(text or "")
    if not matches:
        return None
    return matches[-1].upper()
