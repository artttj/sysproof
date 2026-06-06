from urllib.parse import urlsplit


def extract_domain(url):
    # plausible but wrong: always keeps the last two labels, so a multi-label
    # public suffix like "co.uk" gets mangled into "co.uk" instead of "bbc.co.uk".
    host = (urlsplit(url).hostname or "").lower().strip(".")
    labels = host.split(".")
    return ".".join(labels[-2:])
