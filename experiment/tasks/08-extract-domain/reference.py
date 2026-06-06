from urllib.parse import urlsplit

_MULTI_SUFFIXES = {"co.uk", "com.au", "co.jp"}


def extract_domain(url):
    host = urlsplit(url).hostname or ""
    host = host.lower().strip(".")
    labels = host.split(".")
    if len(labels) >= 3 and ".".join(labels[-2:]) in _MULTI_SUFFIXES:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])
