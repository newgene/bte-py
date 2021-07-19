from tornado.testing import AsyncHTTPTestCase
from biothings_explorer.trapi.biothings import make_test_app
import json
import os


class TestV1QueryByApiEndpoint(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def test_input_query_graph_that_doesnt_pass_swagger_validation_should_return_400(self):
        invalid_input_query_graph = {
            'message1': 1
        }
        response = self.fetch('/v1/smartapi/5be0f321a829792e934545998b9c6afe/query', method="POST", body=json.dumps(invalid_input_query_graph))
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
            response = self.fetch('/v1/smartapi/5be0f321a829792e934545998b9c6afe/query', method='POST', body=json.dumps(query_with_nodes_undefined))
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
            response = self.fetch('/v1/smartapi/5be0f321a829792e934545998b9c6afe/query', method='POST',
                                  body=json.dumps(query_with_edges_undefined))
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
            response = self.fetch('/v1/smartapi/5be0f321a829792e934545998b9c6afe/query', method='POST',
                                  body=json.dumps(query_with_nodes_and_edges_not_match))
            self.assertEqual(response.code, 400)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    def test_query_to_text_mining_targeted_association_kp_should_have_id_resolution_turned_off(self):
        query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'textmining', 'query_chemicals_related_to_gene_or_gene_product.json'))
        with open(query_path) as f:
            query = json.load(f)
            response = self.fetch('/v1/smartapi/978fe380a147a8641caf72320862697b/query', method='POST',
                                  body=json.dumps(query))
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('CHEBI:32677', data['message']['knowledge_graph']['nodes'])
            self.assertEqual(data['message']['knowledge_graph']['nodes']['CHEBI:32677']['attributes'][0]['value'], ["CHEBI:32677"])

    # TODO FIX ME tornado.simple_httpclient.HTTPTimeoutError: Timeout during request
    def test_query_to_non_text_mining_kps_should_have_id_resolution_turned_on(self):
        query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'serviceprovider', 'mychem.json'))
        with open(query_path) as f:
            query = json.load(f)
            response = self.fetch('/v1/smartapi/8f08d1446e0bb9c2b323713ce83e2bd3/query', method='POST',
                                  body=json.dumps(query))
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('NCBIGene:6530', data['message']['knowledge_graph']['nodes'])

    # TODO FIX ME
    # returns 400
    # 'message' not found in data
    def test_query_to_text_mining_cooccurence_kp_should_be_correctly_paginated(self):
        query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'textmining',
                         'query_chemicals_related_to_disease.json'))
        with open(query_path) as f:
            query = json.load(f)
            api_response = self.fetch('https://biothings.ncats.io/text_mining_co_occurrence_kp/query?q=object.id:%22MONDO:0005252%22%20AND%20subject.type:%22ChemicalSubstance%22')
            api_data = json.loads(api_response.body.decode('utf-8'))
            hits = api_data['total']
            response = self.fetch('/v1/smartapi/5be0f321a829792e934545998b9c6afe/query', method='POST',
                                  body=json.dumps(query), connect_timeout=360, request_timeout=360)
            data = json.loads(response.body.decode('utf-8'))
            # nodes should be 3k+ items not 300
            # query_results are empty, might have to do something with the updates to the query_graph_handler package
            self.assertEqual(data['message']['knowledge_graph']['nodes']['CHEBI:26404']['attributes'][0]['value'],
                             ['CHEBI:26404'])
            self.assertEqual(len(data['message']['knowledge_graph']['nodes']), hits + 1)
