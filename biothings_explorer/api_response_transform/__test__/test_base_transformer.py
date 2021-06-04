import os
import unittest
import json
from biothings_explorer.api_response_transform.transformers.transformer import BaseTransformer


class TestBaseTransformer(unittest.TestCase):

    def setUp(self):
        response_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'ols', 'response.json'))
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'ols', 'edge.json'))
        with open(response_path) as f1, open(edge_path) as f2:
            self.response = json.load(f1)
            edge = json.load(f2)
            self._input = {
                'response': self.response,
                'edge': edge,
            }

    def test_pair_input_with_api_response(self):
        tf = BaseTransformer(self._input)
        res = tf.pair_input_with_api_response()
        self.assertIn('DOID:9562', res)
        self.assertEqual(len(res['DOID:9562']), 1)

    def test_wrap_function_if_response_is_not_an_array(self):
        tf = BaseTransformer(self._input)
        res = tf.wrap(self.response)
        self.assertIn('_embedded', res)

    def test_wrap_function_if_response_is_an_array(self):
        tf = BaseTransformer(self._input)
        fake = ['1']
        res = tf.wrap(fake)
        self.assertIn('data', res)
        self.assertEqual(['1'], res['data'])

    def test_json_transform_function(self):
        tf = BaseTransformer(self._input)
        res = tf.json_transform(self.response)
        self.assertIn('has_subclass', res)
        self.assertIn('DOID', res['has_subclass'][0])
        self.assertEqual('DOID:0110596', res['has_subclass'][0]['DOID'])
        self.assertEqual('primary ciliary dyskinesia 21', res['has_subclass'][0]['name'])
        self.assertEqual('A primary ciliary dyskinesia that is characterized by autosomal recessive inheritance with a missing Nexin link, infantile onset of chronic sinopulmonary infections, and has_material_basis_in homozygous mutation in the DRC1 gene on chromosome 2p23.', res['has_subclass'][0]['description'])