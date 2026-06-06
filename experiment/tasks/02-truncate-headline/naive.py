def truncate_headline(text, limit):
    if len(text) <= limit:
        return text
    # plausible but wrong: builds up from whole words only, so a single word
    # longer than the limit gets returned intact and overflows.
    words = text.split(" ")
    out = ""
    for w in words:
        candidate = (out + " " + w).strip()
        if len(candidate) + 1 > limit:
            break
        out = candidate
    if not out:
        out = words[0]
    return out + "…"
