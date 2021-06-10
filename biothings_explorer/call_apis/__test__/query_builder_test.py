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

    def test_if_query_params_value_is_not_string(self):
        edge = {
            "query_operation": {
                "server": "https://google.com",
                "path": "/{geneid}/query",
                "path_params": ["geneid"],
                "params": {
                    "geneid": "hello",
                    "output": 1
                }
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_params(edge, '1017')
        self.assertEqual(res['output'], 1)

    def test_if_request_body_is_empty(self):
        edge = {
            "query_operation": {
                "server": "https://google.com",
                "path": "/{geneid}/query",
                "path_params": ["geneid"],
                "params": {
                    "geneid": "hello",
                    "output": 1
                }
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_request_body(edge, '1017')
        self.assertIsNone(res, None)

    def test_if_request_body_is_not_empty(self):
        edge = {
            "query_operation": {
                "server": "https://google.com",
                "path": "/{geneid}/query",
                "request_body": {
                    "body": {
                        "geneid": "hello",
                        "output": 1
                    }
                }
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_request_body(edge, '1017')
        self.assertEqual(res, {'geneid': 'hello', 'output': 1})

    def test_if_request_body_is_not_empty_and_should_be_replaced_with_input(self):
        edge = {
            "query_operation": {
                "server": "https://google.com",
                "path": "/{geneid}/query",
                "request_body": {
                    "body": {
                        "geneid": "hello",
                        "output": "{inputs[0]}"
                    }
                }
            }
        }
        builder = QueryBuilder(edge)
        res = builder._get_request_body(edge, '1017')
        self.assertEqual(res, {'geneid': 'hello', 'output': '1017'})

    # TODO axios is not a thing in python, need to change this
    def test_construct_axios_request_config_function(self):
        edge = {
            "input": "1017",
            "query_operation": {
                "server": "https://google.com",
                "path": "/{geneid}/query",
                "path_params": ["geneid"],
                "params": {
                    "geneid": "{inputs[0]}",
                    "output": "json"
                },
                "method": "get"
            }
        }
        builder = QueryBuilder(edge)
        #res = builder.construct_request_config()

    def test_non_biothings_tagged_api_should_return_false(self):
        edge = {
            "query_operation": {
                "method": "get",
            },
            "tags": ["translator"]
        }
        response = {
            'total': 1000,
            'hits': [i for i in range(400)]
        }
        builder = QueryBuilder(edge)
        res = builder.need_pagination(response)
        self.assertFalse(res)

    def test_biothings_tagged_api_with_post_method_should_return_false(self):
        edge = {
            "query_operation": {
                "method": "post",
            },
            "tags": ["translator", "biothings"]
        }
        response = {
            'total': 1000,
            'hits': [i for i in range(400)]
        }
        builder = QueryBuilder(edge)
        res = builder.need_pagination(response)
        self.assertFalse(res)

    def test_biothings_tagged_api_with_get_method_needs_pagination_should_return_true(self):
        edge = {
            "query_operation": {
                "method": "get",
            },
            "tags": ["translator", "biothings"]
        }
        response = {
            'total': 1000,
            'hits': [i for i in range(400)]
        }
        builder = QueryBuilder(edge)
        res = builder.need_pagination(response)
        self.assertTrue(res)

    def test_biothings_tagged_api_with_get_method_and_doesnt_need_pagination_should_return_false(self):
        edge = {
            "query_operation": {
                "method": "get",
            },
            "tags": ["translator", "biothings"]
        }
        response = {
            'total': 1000,
            'hits': [i for i in range(1000)]
        }
        builder = QueryBuilder(edge)
        res = builder.need_pagination(response)
        self.assertFalse(res)
