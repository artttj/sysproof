from datetime import datetime, timezone


def to_iso_z(dt):
    """Newsroom convention: all timestamps render as UTC ISO-8601 with a 'Z' suffix
    and second precision, e.g. '2026-06-06T14:30:00Z'. Never '+00:00', never micros."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc).replace(microsecond=0)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
