import os
import unittest
import json
from biothings_explorer.api_response_transform.transformers.ctd_transformer import CTDTransformer


class TestCtdTransformer(unittest.TestCase):
    def setUp(self):
        response_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'ctd', 'response.json'))
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'ctd', 'edge.json'))
        with open(response_path) as f1, open(edge_path) as f2:
            self.response = json.load(f1)
            edge = json.load(f2)
            self._input = {
                'response': self.response,
                'edge': edge,
            }

    def test_ctd_wrapper(self):
        tf = CTDTransformer(self._input)
        res = tf.wrap(self.response)
        self.assertIn('data', res)
        self.assertEquals(len(res['data']), 2)
        self.assertEquals(res['data'][0]['PubMedIDs'], ["21559390"])
        self.assertEquals(res['data'][0]['DiseaseID'], "D008545")

    def test_ctd_wrapper_if_pubmed_id_field_is_not_string(self):
        tf = CTDTransformer(self._input)
        fake = [
            {
                'DiseaseID': "MESH:D008545"
            }
        ]
        res = tf.wrap(fake)
        self.assertIn('data', res)
        self.assertEquals(len(res['data']), 1)
        self.assertIsNone(res['data'][0].get('PubMedIDs'))

    def test_ctd_wrapper_if_disease_id_field_is_not_string(self):
        tf = CTDTransformer(self._input)
        fake = [
            {
                'PubMedID': "12345"
            }
        ]
        res = tf.wrap(fake)
        self.assertIn('data', res)
        self.assertEquals(len(res['data']), 1)
        self.assertIsNone(res['data'][0].get('DiseaseIDs'))
