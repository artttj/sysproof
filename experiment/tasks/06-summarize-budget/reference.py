def fit_to_budget(text, budget=280):
    if len(text) <= budget:
        return text
    words = text.split()
    out = ""
    for w in words:
        candidate = w if not out else out + " " + w
        if len(candidate) > budget:
            break
        out = candidate
    return out
