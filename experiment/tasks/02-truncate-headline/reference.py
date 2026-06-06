def truncate_headline(text, limit):
    if len(text) <= limit:
        return text
    budget = limit - 1  # room for the ellipsis
    head = text[:budget]
    cut = head.rfind(" ")
    if cut > 0:
        head = head[:cut]
    else:
        head = head  # no word boundary: hard cut at budget
    return head.rstrip() + "…"
