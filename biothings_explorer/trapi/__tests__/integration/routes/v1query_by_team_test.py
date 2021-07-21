from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado import ioloop
from biothings_explorer.trapi.biothings import make_test_app
import requests
import json
import os


class TestV1QueryByTeamEndpoint(AsyncHTTPTestCase):

    def get_app(self):
        return make_test_app()

    def test_input_query_graph_that_doesnt_pass_swagger_validation_return_400(self):
        invalid_input_query_graph = {
            'message1': 1
        }

        response = self.fetch('/v1/team/Text%20Mining%20Provider/query', method='POST',
                              body=json.dumps(invalid_input_query_graph))
        self.assertEqual(response.code, 400)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Your input query graph is invalid')

    def test_input_query_graph_missing_nodes_definition_should_return_400(self):
        query_with_nodes_undefined_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'invalid',
                         'query_graph_with_nodes_not_specified.json'))
        with open(query_with_nodes_undefined_path) as f:
            query_with_nodes_undefined = json.load(f)
            response = self.fetch('/v1/team/Text%20Mining%20Provider/query', method='POST', body=json.dumps(query_with_nodes_undefined))
            self.assertEqual(response.code, 400)
            self.assertIn('application/json', response.headers['Content-Type'])
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    def test_input_query_graph_missing_edges_definition_should_return_400(self):
        query_with_edges_undefined_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'invalid',
                         'query_graph_with_edges_not_specified.json'))
        with open(query_with_edges_undefined_path) as f:
            query_with_edges_undefined = json.load(f)
            response = self.fetch('/v1/team/Text%20Mining%20Provider/query', method='POST', body=json.dumps(query_with_edges_undefined))
            self.assertEqual(response.code, 400)
            self.assertIn('application/json', response.headers['Content-Type'])
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    def test_input_query_graph_with_nodes_and_edges_mismatch_should_return_400(self):
        query_with_nodes_and_edges_not_match_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'invalid',
                         'query_graph_with_nodes_and_edges_not_match.json'))
        with open(query_with_nodes_and_edges_not_match_path) as f:
            query_with_nodes_and_edges_not_match = json.load(f)
            response = self.fetch('/v1/team/Text%20Mining%20Provider/query', method='POST', body=json.dumps(query_with_nodes_and_edges_not_match))
            self.assertEqual(response.code, 400)
            self.assertIn('application/json', response.headers['Content-Type'])
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    # TODO
    # Index out of range error
    # This happens due to recent changes on the query_graph_handler/query_results
    def test_query_to_text_mining_kps_should_have_id_resolution_turned_off(self):
        query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'textmining',
                         'query_chemicals_related_to_gene_or_gene_product.json'))
        with open(query_path) as f:
            query = json.load(f)
            response = self.fetch('/v1/team/Text%20Mining%20Provider/query', method='POST', body=json.dumps(query))
            self.assertEqual(response.code, 200)
            self.assertIn('application/json', response.headers['Content-Type'])
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('CHEBI:32677', data['message']['knowledge_graph']['nodes'])
            self.assertEqual(data['message']['knowledge_graph']['nodes']['CHEBI:32677']['attributes'][0]['value'],
                             ['CHEBI:32677'])

    def test_query_to_service_provider_kps_should_have_id_resolution_turned_on(self):
        query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'textmining',
                         'query_chemicals_related_to_gene_or_gene_product.json'))
        with open(query_path) as f:
            query = json.load(f)
            response = self.fetch('/v1/team/Service%20Provider/query', method='POST', body=json.dumps(query))
            self.assertEqual(response.code, 200)
            self.assertIn('application/json', response.headers['Content-Type'])
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('CHEBI:32677', data['message']['knowledge_graph']['nodes'])
            self.assertEqual(data['message']['knowledge_graph']['nodes']['CHEBI:32677']['attributes'][0]['value'],
                             ['CHEBI:32677', 'name:glutamine residue'])

    def test_query_to_text_mining_cooccurence_kp_should_be_correctly_paginated(self):
        query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, os.pardir, 'examples', 'v1.1', 'textmining',
                         'query_chemicals_related_to_disease.json'))
        api_response = requests.get('https://biothings.ncats.io/text_mining_co_occurrence_kp/query?q=object.id:%22MONDO:0005252%22%20AND%20subject.type:%22ChemicalSubstance%22')
        api_data = api_response.json()
        hits = api_data['total']
        with open(query_path) as f:
            query = json.load(f)
            response = self.fetch('/v1/team/Text%20Mining%20Provider/query', method='POST', body=json.dumps(query), request_timeout=5000)
            self.assertEqual(response.code, 200)
            self.assertIn('application/json', response.headers['Content-Type'])
            data = json.loads(response.body.decode('utf-8'))
            self.assertEqual(data['message']['knowledge_graph']['nodes']['CHEBI:26404']['attributes'][0]['value'],
                            ['CHEBI:26404'])
            self.assertEqual(len(data['message']['knowledge_graph']['nodes']), hits + 1)
