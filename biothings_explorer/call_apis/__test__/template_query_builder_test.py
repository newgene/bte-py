import unittest
import os
import json
from ..builder.template_query_builder import TemplateQueryBuilder


class TestQueryBuilderClass(unittest.TestCase):
    def test_get_url_if_server_url_has_a_trailing_slash_function(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com/',
                'path': '/query'
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_url(edge, 'hello')
        self.assertEqual(res, 'https://google.com/query')

    def test_get_url_if_server_url_does_not_have_a_trailing_slash_function(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/query'
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_url(edge, 'hello')
        self.assertEqual(res, 'https://google.com/query')

    def test_get_url_if_api_has_path_parameters(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'path_params': ['geneid'],
                'params': {
                    'geneid': '1017',
                    'output': 'json'
                }
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_url(edge, 'hello')
        self.assertEqual(res, 'https://google.com/1017/query')

    def test_get_url_if_api_has_path_parameters2(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/{output}/query',
                'path_params': ['geneid', 'output'],
                'params': {
                    'geneid': '{{queryInputs}}',
                    'output': 'json'
                }
            }
        }

        builder = TemplateQueryBuilder(edge)
        res = builder._get_url(edge, {'queryInputs': 'hello'})
        self.assertEqual(res, 'https://google.com/hello/json/query')

    def test_get_url_if_nunjucks_templates_are_filled(self):
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data',
                         'multi_input_edge.json'))
        with open(edge_path) as f:
            edge = json.load(f)
            builder = TemplateQueryBuilder(edge)
            res = builder._get_url(edge, {
                'specialpath': '/querytest',
                'id': 'MONDO:0005252',
                'fields': ["subject", "association"],
                'queryInputs': ["abc", "def"]
            })
            self.assertEqual(res, 'https://biothings.ncats.io/text_mining_co_occurrence_kp/querytest')

    def test_get_input_if_api_supports_batch_but_only_one_input_provided_as_string(self):
        edge = {
            'input': 'kevin',
            'query_operation': {
                'supportBatch': True
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_input(edge)
        self.assertEqual(res, edge['input'])

    def test_get_input_if_api_supports_batch_and_multiple_inputs_provided_as_an_array(self):
        edge = {
            'input': ["kevin", "xin"],
            'query_operation': {
                'supportBatch': True
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_input(edge)
        self.assertEqual(res, ["kevin", "xin"])

    def test_get_input_if_api_does_not_support_batch_and_one_input_provided(self):
        edge = {
            'input': 'kevin',
            'query_operation': {
                'supportBatch': False
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_input(edge)
        self.assertEqual(res, edge['input'])

    def test_get_params_if_no_path_parameter_is_involved(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'params': {
                    'geneid': '{{queryInputs}}',
                    'output': 'json'
                }
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_params(edge, {'queryInputs': '1017'})
        self.assertIn('geneid', res)
        self.assertEqual(res['geneid'], '1017')

    # TODO fix me
    def test_get_params_if_path_parameter_is_involved(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'path_params': ['geneid'],
                'params': {
                    'geneid': '{inputs[0]}',
                    'output': 'json'
                }
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_params(edge, '1017')
        self.assertNotIn('geneid', res)
        self.assertEqual(res['output'], 'json')

    def test_get_params_if_path_parameter_is_involved_but_input_is_in_query_params(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'path_params': ['geneid'],
                'params': {
                    'geneid': 'hello',
                    'output': '{{queryInputs}}'
                }
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_params(edge, {'queryInputs': '1017'})
        self.assertNotIn('geneid', res)
        self.assertEqual(res['output'], '1017')

    def test_get_params_if_query_params_value_is_not_string(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'path_params': ['geneid'],
                'params': {
                    'geneid': 'hello',
                    'output': 1
                }
            }
        }

        builder = TemplateQueryBuilder(edge)
        res = builder._get_params(edge, '1017')
        self.assertEqual(res['output'], 1)

    def test_get_params_if_jinja_templates_are_filled(self):
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data',
                         'multi_input_edge.json'))
        with open(edge_path) as f:
            edge = json.load(f)
            builder = TemplateQueryBuilder(edge_path)
            res = builder._get_params(edge, {
                'specialpath': '/querytest',
                'id': 'MONDO:0005252',
                'fields': ["subject", "association"],
                'queryInputs': ["abc", "def"]
            })
            self.assertEqual(res, {
                'fields': 'subject,association',
                'q': 'object.MONDO:"MONDO:0005252" AND subject.type:SmallMolecule',
                'size': 1000
            })

    def test_get_request_body_if_request_body_is_empty(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'path_params': ['geneid'],
                'params': {
                    'geneid': 'hello',
                    'output': 1
                }
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_request_body(edge, '1017')
        self.assertIsNone(res)

    def test_get_request_body_if_request_body_is_not_empty(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'request_body': {
                    'body': {
                        'geneid': 'hello',
                        'output': 1
                    }
                }
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_request_body(edge, '1017')
        self.assertEqual(res, 'geneid=hello&output=1')

    def test_get_request_body_if_body_is_not_empty_and_should_be_replaced_with_input(self):
        edge = {
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'request_body': {
                    'body': {
                        'geneid': 'hello',
                        'output': '{{queryInputs}}'
                    }
                }
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder._get_request_body(edge, {'queryInputs': '1017'})
        self.assertEqual(res, 'geneid=hello&output=1017')

    def test_get_request_body_if_jinja_templates_are_filled(self):
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data',
                         'multi_input_edge.json'))
        with open(edge_path) as f:
            edge = json.load(f)
            builder = TemplateQueryBuilder(edge)
            res = builder._get_request_body(edge, {
                'specialpath': '/querytest',
                'id': 'MONDO:0005252',
                'fields': ["subject", "association"],
                'queryInputs': ["abc", "def"]
            })
            self.assertEqual(res, 'q=MONDO:0005252&fields=subject,association')

    def test_construct_axios_request_config(self):
        edge = {
            'input': {'queryInputs': ['1017']},
            'query_operation': {
                'server': 'https://google.com',
                'path': '/{geneid}/query',
                'path_params': ['geneid'],
                'params': {
                    'geneid': '{{queryInputs}}',
                    'output': 'json'
                },
                'method': 'get'
            }
        }
        builder = TemplateQueryBuilder(edge)
        res = builder.construct_axios_request_config()
        #self.assertEqual(res['timeout'], 50000)
        self.assertEqual(res['url'], 'https://google.com/1017/query')
        self.assertNotIn('geneid', res['params'])
        self.assertEqual(res['params']['output'], 'json')
        self.assertEqual(res['method'], 'get')
        self.assertIsNone(res['data'])

    def test_need_pagination_non_biothings_tagged_api_should_return_false(self):
        edge = {
            'query_operation': {
                'method': 'post'
            },
            'tags': ["translator", "biothings"]
        }
        response = {
            'total': 1000,
            'hits': [i for i in range(400)]
        }
        builder = TemplateQueryBuilder(edge)
        res = builder.need_pagination(response)
        self.assertFalse(res)

    def test_need_pagination_biothings_tagged_api_with_post_method_should_return_false(self):
        edge = {
            'query_operation': {
                'method': 'post'
            },
            'tags': ["translator", "biothings"]
        }
        response = {
            'total': 1000,
            'hits': [i for i in range(400)]
        }
        builder = TemplateQueryBuilder(edge)
        res = builder.need_pagination(response)
        self.assertFalse(res)

    def test_need_pagination_biothings_tagged_api_with_get_method_and_needs_pagination_should_return_true(self):
        edge = {
            'query_operation': {
                'method': 'get'
            },
            'tags': ["translator", "biothings"]
        }
        response = {
            'total': 1000,
            'hits': [i for i in range(400)]
        }
        builder = TemplateQueryBuilder(edge)
        res = builder.need_pagination(response)
        self.assertTrue(res)

    def test_need_pagination_biothings_tagged_api_with_get_method_and_doesnt_need_pagination_should_return_false(self):
        edge = {
            'query_operation': {
                'method': 'get'
            },
            'tags': ["translator", "biothings"]
        }
        response = {
            'total': 1000,
            'hits': [i for i in range(1000)]
        }
        builder = TemplateQueryBuilder(edge)
        res = builder.need_pagination(response)
        self.assertFalse(res)
