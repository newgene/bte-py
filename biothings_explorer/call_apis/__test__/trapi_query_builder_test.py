import unittest
from ..builder.trapi_query_builder import TRAPIQueryBuilder


class TestTrapiQueryBuilder(unittest.TestCase):
    def test_if_server_url_has_a_trailing_slash(self):
        edge = {
            "query_operation": {
                "server": "https://google.com/",
                "path": "/query"
            },
            "association": {
                "input_type": 'Pathway',
                "output_type": 'Gene',
                "predicate": 'related_to'
            },
            "input": ['123', '456']
        }
        builder = TRAPIQueryBuilder(edge)
        res = builder.get_config()
        self.assertIn('url', res)
        self.assertEqual(res['url'], 'https://google.com/query')
        #self.assertIn('timeout', res)
        #self.assertEqual(res['timeout'], 3000)
        self.assertEqual(res['params']['message']['query_graph']['nodes']['n0']['ids'], ['123', '456'])
        self.assertIn('biolink:Pathway', res['params']['message']['query_graph']['nodes']['n0']['categories'])
        self.assertIn('biolink:Gene', res['params']['message']['query_graph']['nodes']['n1']['categories'])
        self.assertIn('biolink:related_to', res['params']['message']['query_graph']['edges']['e01']['predicates'])
