You are working in a news pipeline that pulls stories from several feeds. Implement
`dedupe_articles(articles)` that takes a list of article dicts (each has a `"url"`
key) and returns the list with duplicate stories removed, keeping the first
occurrence. The same story often arrives from different feeds with slightly
different URLs.
