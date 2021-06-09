import unittest
from ..builder.query_builder import QueryBuilder


class TestQueryBuilder(unittest.TestCase):
    def test_if_server_url_has_a_trailing_slash(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com/',
                'path': '/query'
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_url(edge, 'hello')
        self.assertEqual(res, 'https://google.com/query')

    def test_if_server_url_does_not_have_a_trailing_slash(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/query'
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_url(edge, 'hello')
        self.assertEqual(res, 'https://google.com/query')

    def test_if_api_has_path_parameters(self):
        edge = {
            'query_operation': {
                "server": "https://google.com",
                "path": "/{geneid}/query",
                "path_params": ["geneid"],
                "params": {
                    "geneid": "1017",
                    "output": "json"
                }
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_url(edge, 'hello')
        self.assertEqual(res, 'https://google.com/1017/query')

    def test_if_api_has_path_parameters2(self):
        edge = {
            "query_operation": {
                "server": "https://google.com",
                "path": "/{geneid}/{output}/query",
                "path_params": ["geneid", "output"],
                "params": {
                    "geneid": "{inputs[0]}",
                    "output": "json"
                }
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_url(edge, 'hello')
        self.assertEqual(res, 'https://google.com/hello/json/query')

    def test_if_api_supports_batch_but_only_one_input_provided_as_string(self):
        edge = {
            "input": "kevin",
            "query_operation": {
                "supportBatch": True,
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_input(edge)
        self.assertEqual(res, edge['input'])

    def test_if_api_supports_batch_and_multiple_inputs_provided_as_an_array(self):
        edge = {
            "input": ["kevin", "xin"],
            "query_operation": {
                "supportBatch": True,
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_input(edge)
        self.assertEqual(res, 'kevin,xin')

    def test_if_api_does_not_supports_batch_and_one_input_provided(self):
        edge = {
            "input": "kevin",
            "query_operation": {
                "supportBatch": False,
            }
        }

        builder = QueryBuilder(edge)
        res = builder._get_input(edge)
        self.assertEqual(res, edge['input'])

    def test_if_no_path_parameter_is_involved(self):
        edge = {
            "query_operation": {
                "server": "https://google.com",
                "path": "/{geneid}/query",
                "params": {
                    "geneid": "{inputs[0]}",
                    "output": "json"
                }
            }
        }

        builder = QueryBuilder(edge)
        res = builder._get_params(edge, '1017')
        self.assertIn('geneid', res)
        self.assertEqual(res['geneid'], '1017')

    def test_if_path_parameter_is_involved(self):
        edge = {
            "query_operation": {
                "server": "https://google.com",
                "path": "/{geneid}/query",
                "path_params": ["geneid"],
                "params": {
                    "geneid": "{inputs[0]}",
                    "output": "json"
                }
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_params(edge, '1017')
        self.assertNotIn('geneid', res)
        self.assertEqual(res['output'], 'json')