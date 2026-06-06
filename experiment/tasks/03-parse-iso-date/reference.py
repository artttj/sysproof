from datetime import date


def parse_iso_date(s):
    parts = s.split("-")
    if len(parts) != 3:
        raise ValueError(f"not an ISO date: {s!r}")
    year, month, day = (int(p) for p in parts)
    date(year, month, day)  # raises ValueError on an impossible calendar date
    return (year, month, day)
