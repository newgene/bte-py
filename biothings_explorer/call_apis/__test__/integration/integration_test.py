import unittest
import os
import requests
import json
from biothings_explorer.call_apis.query import APIQueryDispatcher


class TestIntegrationUsingMygeneInfoGeneToBiologicalProcessAssociation(unittest.TestCase):

    def test_check_response(self):
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'mygene_example_edge.json'))
        with open(edge_path) as f:
            edge = json.load(f)
            query = APIQueryDispatcher([edge])
            res = query.query()
            self.assertEqual(len(res), 29)

    def test_integration_test_using_text_mining_cooccurence_kp_for_disease_to_chemical_association(self):
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'mygene_example_edge.json'))
        with open(edge_path) as f:
            edge = json.load(f)
            query = APIQueryDispatcher([edge])
            res = query.query(False)
            self.assertEqual(len(res), 3762)

    def test_integration_test_using_fake_error_api_query_that_should_return_404_error(self):
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'mygene_example_edge.json'))
        with open(edge_path) as f:
            edge = json.load(f)
            query = APIQueryDispatcher([edge])
            res = query.query(False)
            self.assertEqual(len(res), 0)
