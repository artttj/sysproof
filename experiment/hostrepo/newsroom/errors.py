class FeedError(Exception):
    """All recoverable feed problems raise FeedError, never ValueError. Call sites
    catch FeedError specifically; a ValueError escapes and crashes the worker."""

    def __init__(self, code, message):
        self.code = code
        super().__init__(f"[{code}] {message}")
