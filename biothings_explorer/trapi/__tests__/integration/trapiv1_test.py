import unittest
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado import ioloop
from biothings_explorer.trapi.biothings import make_test_app
import requests
import json
import os


class TestV1Endpoints(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    @unittest.skip('deprecated endpoint')
    def test_v1_predicates(self):
        response = self.fetch('/v1/predicates')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('biolink:Gene', data)
        self.assertIn('biolink:ChemicalSubstance', data['biolink:Gene'])
        self.assertIn('biolink:related_to', data['biolink:Gene']['biolink:ChemicalSubstance'])

    @unittest.skip('deprecated endpoint')
    def test_v1_smartapi_predicates(self):
        response = self.fetch('/v1/smartapi/978fe380a147a8641caf72320862697b/predicates')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('biolink:Gene', data)
        self.assertIn('biolink:ChemicalSubstance', data['biolink:Gene'])

    @unittest.skip("Using outdated query_graph_handler version")
    def test_post_v1_query_with_gene2chemical_query(self):
        gene2chemical_query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v1',
                         'query_chemicals_physically_interacts_with_genes.json'))

        with open(gene2chemical_query_path) as f:
            gene2chemical_query = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(gene2chemical_query))
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('query_graph', data['message'])
            self.assertIn('knowledge_graph', data['message'])
            self.assertIn('nodes', data['message']['knowledge_graph'])
            self.assertIn('edges', data['message']['knowledge_graph'])
            self.assertIn('NCBIGene:1017', data['message']['knowledge_graph']['nodes'])

    @unittest.skip("Using outdated query_graph_handler version")
    def test_post_v1_query_with_clinical_risk_kp_query(self):
        drug2disease_query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v1', 'multiomics', 'clinical_risk_kp',
                         'query_drug_to_disease.json'))
        with open(drug2disease_query_path) as f:
            drug2disease_query = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(drug2disease_query))
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('query_graph', data['message'])
            self.assertIn('knowledge_graph', data['message'])
            self.assertIn('nodes', data['message']['knowledge_graph'])
            self.assertIn('edges', data['message']['knowledge_graph'])
            self.assertIn('MONDO:0001583', data['message']['knowledge_graph']['nodes'])

    def test_post_v1_query_with_query_graph_defined_in_old_trapi_standard(self):
        query_using_earlier_trapi_spec_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v0.9.2', 'query_genes_relate_to_disease.json'))
        with open(query_using_earlier_trapi_spec_path) as f:
            query_using_earlier_trapi_spec = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(query_using_earlier_trapi_spec))
            self.assertEqual(response.code, 400)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('error', data)
            self.assertEqual(data['error'], 'Your input query graph is invalid')

    @unittest.skip("Using outdated query_graph_handler version")
    def test_post_v1_query_with_disease2gene_query(self):
        disease2gene_query_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v1', 'query_genes_relate_to_disease.json'))
        with open(disease2gene_query_path) as f:
            disease2gene_query = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(disease2gene_query))
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('application/json', response.headers['Content-Type'])
            self.assertIn('message', data)
            self.assertIn('query_graph', data['message'])
            self.assertIn('knowledge_graph', data['message'])
            self.assertIn('nodes', data['message']['knowledge_graph'])
            self.assertIn('edges', data['message']['knowledge_graph'])
            self.assertIn('MONDO:0005737', data['message']['knowledge_graph']['nodes'])

    @unittest.skip("Using outdated query_graph_handler version")
    def test_post_v1_query_with_query_that_doesnt_provide_input_category(self):
        query_without_category_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         os.pardir, os.pardir, 'examples', 'v1', 'query_without_input_category.json'))
        with open(query_without_category_path) as f:
            query_without_category = json.load(f)
            response = self.fetch('/v1/query', method='POST', body=json.dumps(query_without_category))
            self.assertEqual(response.code, 200)
            data = json.loads(response.body.decode('utf-8'))
            self.assertIn('message', data)
            self.assertIn('query_graph', data['message'])
            self.assertIn('knowledge_graph', data['message'])
            self.assertIn('nodes', data['message']['knowledge_graph'])
            self.assertIn('edges', data['message']['knowledge_graph'])
            self.assertIn('MONDO:0016575', data['message']['knowledge_graph']['nodes'])
            self.assertIn('UMLS:C0008780', data['message']['knowledge_graph']['nodes'])
            self.assertIn('category', data['message']['knowledge_graph']['nodes']['UMLS:C0008780'])
            self.assertEqual(data['message']['knowledge_graph']['nodes']['UMLS:C0008780']['category'], 'biolink:PhenotypicFeature')
