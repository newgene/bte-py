import unittest
import os
import requests
import json
from biothings_explorer.call_apis.query import APIQueryDispatcher


class TestIntegrationUsingMygeneInfoGeneToBiologicalProcessAssociation(unittest.TestCase):
    def setUp(self):
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'mygene_example_edge.json'))
        with open(edge_path) as f:
            self.edge = json.load(f)

    def test_check_response(self):
        query = APIQueryDispatcher([self.edge])
        res = query.query()
        self.assertEqual(len(res), 29)
