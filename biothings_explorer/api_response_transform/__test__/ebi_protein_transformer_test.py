import os
import unittest
import json
from biothings_explorer.api_response_transform.transformers.ebi_protein_transformer import EBIProteinTransformer


class TestEbiProteinTransformer(unittest.TestCase):
    def setUp(self):
        response_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'ebi_protein', 'response.json'))
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'ebi_protein', 'edge.json'))
        with open(response_path) as f1, open(edge_path) as f2:
            self.response = json.load(f1)
            edge = json.load(f2)
            self._input = {
                'response': self.response,
                'edge': edge,
            }

    def test_ebi_wrapper(self):
        tf = EBIProteinTransformer(self._input)
        res = tf.wrap(self.response)
        self.assertEquals(len(res['comments'][0]['reaction']['dbReferences']), 1)
