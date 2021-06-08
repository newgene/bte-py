from .query_bucket import QueryBucket


class APIQueryQueue:
    def __init__(self, queries):
        self.queue = []
        self.queries = queries

    def dequeue(self):
        self.queue.pop(0)

    def add_query(self, query):
        for bucket in self.queue:
            if bucket.can_be_added(query.get_url()):
                bucket.add(query)
                return
        new_bucket = QueryBucket()
        new_bucket.add(query)
        self.queue.append(new_bucket)

    def construct_queue(self, queries):
        for query in queries:
            self.add_query(query)
