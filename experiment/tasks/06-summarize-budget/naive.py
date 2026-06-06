def fit_to_budget(text, budget=280):
    # plausible but wrong: reads "budget" as a word count instead of a character
    # count, so long texts with few words blow past the character limit.
    words = text.split()
    if len(words) <= budget:
        return text
    return " ".join(words[:budget])
