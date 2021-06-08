class QueryBucket:
    def __init__(self):
        self.cnt = {}
        self.bucket = []
        self.MAX_CONCURRENT_API_QUERIES = 3

    def can_be_added(self, url):
        if not (url in self.cnt) or self.cnt[url] < self.MAX_CONCURRENT_API_QUERIES:
            return True
        return False

    def add(self, query):
        if not (query.get_url() in self.cnt):
            self.cnt[query.get_url()] = 0
        self.cnt[query.get_url()] += 1
        self.bucket.append(query)

    def get_bucket(self):
        return self.bucket
