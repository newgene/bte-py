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
