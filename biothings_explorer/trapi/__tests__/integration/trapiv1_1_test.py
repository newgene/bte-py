import unittest
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado import ioloop
from biothings_explorer.trapi.biothings import make_test_app
import requests
import json
import os


class TestV1_1Endpoints(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def test_get_v1_meta_knowledge_graph(self):
        response = self.fetch('/v1/meta_knowledge_graph')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('nodes', data)
        self.assertIn('biolink:Gene', data['nodes'])
        self.assertIn('id_prefixes', data['nodes']['biolink:Gene'])
        self.assertIn('edges', data)
        assertion_item = {
            "subject": "biolink:ChemicalSubstance",
            "predicate": "biolink:entity_positively_regulates_entity",
            "object": "biolink:Gene"
        }
        # check if this "assertion_item" object is a subset on any of the data['edges'] items
        check_for_subset = [True if assertion_item.items() <= item.items() else False for item in data['edges']]
        self.assertTrue(any(check_for_subset))

    def test_get_v1_team_meta_knowledge_graph(self):
        response = self.fetch('/v1/team/Service%20Provider/meta_knowledge_graph')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('nodes', data)
        self.assertIn('biolink:Gene', data['nodes'])
        self.assertIn('id_prefixes', data['nodes']['biolink:Gene'])
        self.assertIn('edges', data)
        assertion_item = {
            "subject": "biolink:SequenceVariant",
            "predicate": "biolink:located_in",
            "object": "biolink:Gene",
        }
        check_for_subset = [True if assertion_item.items() <= item.items() else False for item in data['edges']]
        self.assertTrue(any(check_for_subset))

    def test_query_text_mining_team_should_return_200_with_valid_response(self):
        response = self.fetch('/v1/team/Text%20Mining%20Provider/meta_knowledge_graph')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('nodes', data)
        self.assertIn('biolink:Gene', data['nodes'])
        assertion_item = {
            "subject": "biolink:ChemicalSubstance",
            "predicate": "biolink:entity_positively_regulates_entity",
            "object": "biolink:Gene",
        }
        check_for_subset = [True if assertion_item.items() <= item.items() else False for item in data['edges']]
        self.assertTrue(any(check_for_subset))

    # returns 200 but expects 404?
    def test_query_to_invalid_team_should_return_200_with_empty_response(self):
        response = self.fetch('/v1/team/wrong%20team/meta_knowledge_graph')
        self.assertEqual(response.code, 404)

    def test_get_v1_smart_api_metaknowledge_graph(self):
        response = self.fetch('/v1/smartapi/978fe380a147a8641caf72320862697b/meta_knowledge_graph')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('nodes', data)
        self.assertIn('biolink:Protein', data['nodes'])
        assertion_item = {
            "subject": "biolink:ChemicalSubstance",
            "predicate": "biolink:entity_positively_regulates_entity",
            "object": "biolink:Gene"
        }
        check_for_subset = [True if assertion_item.items() <= item.items() else False for item in data['edges']]
        self.assertTrue(any(check_for_subset))

    # def test_query_to_invalid_api_should_return_404_with_error_message_included(self):
    #     response = self.fetch('/v1/smartapi/78fe380a147a8641caf72320862697b/meta_knowledge_graph')
    #     self.assertEqual(response.code, 404)
    #     data = json.loads(response.body.decode('utf-8'))
    #     self.assertIn('application/json', response.headers['Content-Type'])
    #     # TODO handle these exceptions
    #     self.assertIn('error', data)
    #     self.assertEqual(data['error'], 'Unable to load predicates')
    #     self.assertIn('more_info', data)
    #     self.assertEqual(data['more_info'], 'Failed to Load MetaKG: PredicatesLoadingError: Not Found - 0 operations')

    def test_get_v1_smartapi_meta_knowledge_graph(self):
        response = self.fetch('/v1/smartapi/978fe380a147a8641caf72320862697b/meta_knowledge_graph')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('nodes', data)
        self.assertIn('biolink:Protein', data['nodes'])
        assertion_item = {
            "subject": "biolink:ChemicalSubstance",
            "predicate": "biolink:entity_positively_regulates_entity",
            "object": "biolink:Gene"
        }
        check_for_subset = [True if assertion_item.items() <= item.items() else False for item in data['edges']]
        self.assertTrue(any(check_for_subset))

    def test_query_to_invalid_api_should_return_404_with_error_message_included(self):
        response = self.fetch('/v1/smartapi/78fe380a147a8641caf72320862697b/meta_knowledge_graph')
        self.assertEqual(response.code, 404)
        data = json.loads(response.body.decode('utf-8'))
        # TODO handle these exceptions
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Unable to load predicates')
        self.assertIn('more_info', data)
        self.assertEqual(data['more_info'], 'Failed to Load MetaKG: PredicatesLoadingError: Not Found - 0 operations')

    def test_post_v1_query_with_gene2chemical_query(self):
        gene2chemical_query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v1.1', 'query_chemicals_physically_interacts_with_genes.json'))
        with open(gene2chemical_query_path) as f:
            gene2chemical_query = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(gene2chemical_query), request_timeout=5000)
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('query_graph', data['message'])
            self.assertIn('nodes', data['message']['knowledge_graph'])
            self.assertIn('edges', data['message']['knowledge_graph'])
            self.assertIn('NCBIGene:1017', data['message']['knowledge_graph']['nodes'])

    @unittest.skip
    def test_post_v1_query_with_clinical_risk_kp_query(self):
        drug2disease_query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v1.1', 'multiomics', 'clinical_risk_kp', 'query_drug_to_disease.json'))
        with open(drug2disease_query_path) as f:
            drug2disease_query = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(drug2disease_query), request_timeout=5000)
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('query_graph', data['message'])
            self.assertIn('knowledge_graph', data['message'])
            self.assertIn('nodes', data['message']['knowledge_graph'])
            self.assertIn('edges', data['message']['knowledge_graph'])
            self.assertIn('MONDO:0001583', data['message']['knowledge_graph']['nodes'])

    def test_post_v1_query_with_query_defined_in_old_trapi_standard(self):
        query_using_earlier_trapi_spec_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v0.9.2', 'query_genes_relate_to_disease.json'))
        with open(query_using_earlier_trapi_spec_path) as f:
            query_using_earlier_trapi_spec = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(query_using_earlier_trapi_spec), request_timeout=5000)
            self.assertEqual(response.code, 400)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    # TODO
    # node not in nodes, issue with the query_graph_handler package
    def test_post_v1_query_with_disease2gene_query(self):
        disease2gene_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v1.1', 'query_genes_relate_to_disease.json'))
        with open(disease2gene_path) as f:
            disease2gene_path = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(disease2gene_path), request_timeout=5000)
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('message', data)
            self.assertIn('query_graph', data['message'])
            self.assertIn('knowledge_graph', data['message'])
            self.assertIn('nodes', data['message']['knowledge_graph'])
            self.assertIn('edges', data['message']['knowledge_graph'])
            self.assertIn('MONDO:0005737', data['message']['knowledge_graph']['nodes'])

    # TODO
    # node not in nodes, issue with the query_graph_handler package
    def test_post_v1_query_with_query_that_doesnt_provide_input_category(self):
        query_without_category_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v1.1', 'query_without_input_category.json'))
        with open(query_without_category_path) as f:
            query_without_category = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(query_without_category), request_timeout=5000)
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('message', data)
            self.assertIn('query_graph', data['message'])
            self.assertIn('knowledge_graph', data['message'])
            self.assertIn('nodes', data['message']['knowledge_graph'])
            self.assertIn('edges', data['message']['knowledge_graph'])
            self.assertIn('MONDO:0016575', data['message']['knowledge_graph']['nodes'])
            self.assertIn('UMLS:C0008780', data['message']['knowledge_graph']['nodes'])
            self.assertIn('categories', data['message']['knowledge_graph']['nodes']['UMLS:C0008780'])
            self.assertEqual(data['message']['knowledge_graph']['nodes']['UMLS:C0008780']['categories'], ['biolink:PhenotypicFeature'])
