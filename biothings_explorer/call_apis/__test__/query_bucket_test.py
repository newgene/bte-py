import unittest
from ..query_bucket import QueryBucket


class TestQueryBucket(unittest.TestCase):
    def test_can_be_added_function(self):
        bucket = QueryBucket()
        res = bucket.can_be_added('k')
        self.assertEqual(res, True)

    def test_return_true_if_item_to_be_added_has_not_reached_max_cnt_yet(self):
        bucket = QueryBucket()
        bucket.cnt = {'k': bucket.MAX_CONCURRENT_API_QUERIES - 1}
        res = bucket.can_be_added('k')
        self.assertEqual(res, True)

    def test_return_false_it_item_to_be_added_has_reached_max_cnt_yet(self):
        bucket = QueryBucket()
        bucket.cnt = {'k': bucket.MAX_CONCURRENT_API_QUERIES}
        res = bucket.can_be_added('k')
        self.assertEqual(res, False)

    def test_return_false_if_item_to_be_added_has_exceeded_max_cnt_yet(self):
        bucket = QueryBucket()
        bucket.cnt = {'k': bucket.MAX_CONCURRENT_API_QUERIES + 1}
        res = bucket.can_be_added('k')
        self.assertEqual(res, False)

    def test_if_query_has_not_been_in_the_bucket_before(self):
        bucket = QueryBucket()

        class Query:
            def get_url(self):
                return 'hello'

        query = Query()
        bucket.add(query)
        self.assertEqual(bucket.cnt['hello'], 1)
        self.assertEqual(len(bucket.bucket), 1)

    def test_if_query_has_not_been_in_the_bucket_before(self):
        bucket = QueryBucket()

        class Query:
            def get_url(self):
                return 'hello'

        class Query2:
            def get_url(self):
                return 'kitty'

        query = Query()
        query1 = Query2()

        bucket.add(query)
        bucket.add(query)
        bucket.add(query1)
        self.assertEqual(bucket.cnt['hello'], 2)
        self.assertEqual(bucket.cnt['kitty'], 1)
        self.assertEqual(len(bucket.bucket), 3)

    def test_get_bucket_function(self):
        bucket = QueryBucket()
        bucket.bucket = [1]
        self.assertEqual(bucket.get_bucket(), [1])
