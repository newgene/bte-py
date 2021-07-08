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