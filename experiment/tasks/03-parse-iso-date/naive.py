def parse_iso_date(s):
    # plausible but wrong: checks shape and int-conversion but never validates
    # that the month/day are in range, so "2026-13-01" slips through.
    parts = s.split("-")
    if len(parts) != 3:
        raise ValueError(f"not an ISO date: {s!r}")
    year, month, day = (int(p) for p in parts)
    return (year, month, day)
