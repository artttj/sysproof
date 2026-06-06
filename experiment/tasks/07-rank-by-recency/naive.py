def rank_by_recency(articles):
    # plausible but wrong: treats a missing timestamp as "very recent" so unknown
    # articles float to the top instead of sinking to the bottom.
    return sorted(
        articles,
        key=lambda a: a["ts"] if a.get("ts") is not None else float("inf"),
        reverse=True,
    )
