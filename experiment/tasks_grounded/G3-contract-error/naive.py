def require_field(item, field):
    if not item.get(field):
        raise ValueError(f"missing {field}")
    return True
