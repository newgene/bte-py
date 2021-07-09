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
        self.assertIn('nodes.biolink:Gene', data)
        self.assertIn('nodes.biolink:Gene.id_prefixes', data)
        self.assertIn('edges', data)
        assertion_item = {
            "subject": "biolink:ChemicalSubstance",
            "predicate": "biolink:entity_positively_regulates_entity",
            "object": "biolink:Gene"
          }
        # check if this "assertion_item" object is a subset on any of the data['edges'] items
        self.assertTrue(any([True if all(dict_item in item.items() for dict_item in assertion_item.items()) else False for item in data['edges']]))
