from tornado.testing import AsyncHTTPTestCase
from biothings_explorer.trapi.biothings import make_test_app
import json
import os


class TestQueryEndpoint(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def test_input_query_graph_that_doesnt_pass_swagger_validation_should_return_400_error(self):
        invalid_input_query_graph = {
            'message': 1
        }
        response = self.fetch('/v1/query', method="POST", body=json.dumps(invalid_input_query_graph))
        self.assertEqual(response.code, 400)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Your input query graph is invalid')

    def test_input_query_graph_missing_nodes_definition_should_return_400(self):
        query_with_nodes_undefined_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'invalid', 'query_graph_with_nodes_not_specified.json'))

        with open(query_with_nodes_undefined_path) as f:
            query_with_nodes_undefined = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(query_with_nodes_undefined))
            self.assertEqual(response.code, 400)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    def test_input_query_graph_missing_edges_definition_should_return_400(self):
        query_with_edges_undefined_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'invalid', 'query_graph_with_edges_not_specified.json'))
        with open(query_with_edges_undefined_path) as f:
            query_with_edges_undefined = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(query_with_edges_undefined))
            self.assertEqual(response.code, 400)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    def test_input_query_graph_with_nodes_and_edges_mismatch_should_return_400(self):
        query_with_nodes_and_edges_not_match_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'invalid', 'query_graph_with_nodes_and_edges_not_match.json'))
        with open(query_with_nodes_and_edges_not_match_path) as f:
            query_with_nodes_and_edges_not_match = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(query_with_nodes_and_edges_not_match))
            self.assertEqual(response.code, 400)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    # TODO FIX ME: there is a problem with the query returning no results, probably has to do with
    # the query_graph_handler package
    # js package also fails on this test
    def test_multi_hop_query_results_should_have_combined_edges(self):
        query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'query_multihop_gene_gene_chemical.json'))
        with open(query_path) as f:
            query = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(query))
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertEqual(data['message']['results'][0]['node_bindings'].keys(), ['n0', 'n1', 'n2'])
            self.assertEqual(data['message']['results'][0]['edge_bindings'].keys(), ['e01', 'e02'])
