import unittest
from ..query_bucket import QueryBucket
from ..query_queue import APIQueryQueue


class TestQueryQueueModule(unittest.TestCase):
    def test_dequeue_function(self):
        queue = APIQueryQueue([])
        queue.queue = [1, 2]
        queue.dequeue()
        self.assertEqual(queue.queue, [2])

    def test_dequeue_function_if_queue_is_empty(self):
        queue = APIQueryQueue([])
        queue.queue = []
        queue.dequeue()
        self.assertEqual(queue.queue, [])

    def test_create_a_new_bucket_with_the_query_when_queue_is_empty(self):
        queue = APIQueryQueue([])

        class Query:
            def get_url(self):
                return 'hello'

        query = Query()
        queue.add_query(query)
        self.assertEqual(len(queue.queue), 1)
        self.assertIsInstance(queue.queue[0], QueryBucket)
        self.assertEqual(len(queue.queue[0].bucket), 1)
        self.assertEqual(queue.queue[0].bucket[0], query)

    def test_create_a_new_bucket_when_query_exceeds_maximum_in_a_bucket(self):
        queue = APIQueryQueue([])

        class Query:
            def get_url(self):
                return 'hello'

        query = Query()
        queue.add_query(query)
        self.assertEqual(len(queue.queue), 1)
        queue.add_query(query)
        self.assertEqual(len(queue.queue), 1)
        queue.add_query(query)
        self.assertEqual(len(queue.queue), 1)
        queue.add_query(query)
        self.assertEqual(len(queue.queue), 2)
        self.assertIsInstance(queue.queue[1], QueryBucket)
        self.assertEqual(len(queue.queue[0].bucket), 3)
        self.assertEqual(len(queue.queue[1].bucket), 1)
        self.assertEqual(queue.queue[0].bucket[0], query)

    def test_with_query_size_of_1(self):
        queue = APIQueryQueue([])

        class Query:
            def get_url(self):
                return 'hello'

        query = Query()
        queue.construct_queue([query])
        self.assertEqual(len(queue.queue), 1)

    def test_input_with_mixed_queries(self):
        queue = APIQueryQueue([])

        class Query:
            def get_url(self):
                return 'hello'

        class Query2:
            def get_url(self):
                return 'hello kitty'

        query1 = Query()
        query2 = Query2()
        queue.construct_queue([query1, query2, query1, query1, query2, query1])
        self.assertEqual(len(queue.queue), 2)
        self.assertEqual(len(queue.queue[0].bucket), 5)
        self.assertEqual(len(queue.queue[1].bucket), 1)
        