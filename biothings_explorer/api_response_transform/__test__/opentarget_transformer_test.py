import os
import unittest
import json
from biothings_explorer.api_response_transform.transformers.opentarget_transformer import OpenTargetTransformer


class TestOpenTargetTransformer(unittest.TestCase):
    def setUp(self):
        response_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'opentarget', 'response.json'))
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'opentarget', 'edge.json'))
        with open(response_path) as f1, open(edge_path) as f2:
            self.response = json.load(f1)
            edge = json.load(f2)
            self._input = {
                'response': self.response,
                'edge': edge,
            }

    def test_opentarget_wrapper(self):
        tf = OpenTargetTransformer(self._input)
        res = tf.wrap(self.response)
        self.assertIn('data', res)
        self.assertEquals(res['data'][0]['drug']['id'], 'CHEMBL220492')

    def test_opentarget_wrapper_if_id_is_not_chembl(self):
        tf = OpenTargetTransformer(self._input)
        fake = {
            'data': [
                {
                    'drug': {
                        'id': "http://identifiers.org/drugbank/DB0001"
                    }
                }
            ]
        }
        res = tf.wrap(fake)
        self.assertIn('data', res)
        self.assertEquals(res['data'][0]['drug']['id'], "http://identifiers.org/drugbank/DB0001")
