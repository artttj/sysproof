def merge_translations(base, overrides):
    # plausible but wrong: a shallow merge. When both sides have a dict under the
    # same key, the override's subtree replaces the base's wholesale, dropping any
    # base-only nested keys.
    return {**base, **overrides}
