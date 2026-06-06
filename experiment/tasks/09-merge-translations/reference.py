def merge_translations(base, overrides):
    out = dict(base)
    for key, value in overrides.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = merge_translations(out[key], value)
        else:
            out[key] = value
    return out
