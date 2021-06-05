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
        self.assertEqual(['A primary ciliary dyskinesia that is characterized by autosomal recessive inheritance with a missing Nexin link, infantile onset of chronic sinopulmonary infections, and has_material_basis_in homozygous mutation in the DRC1 gene on chromosome 2p23.'], res['has_subclass'][0]['description'])

    def test_update_publications_function_if_pubmed_id_is_prefixed(self):
        tf = BaseTransformer(self._input)
        fake = {
            'pubmed': 'PMID:1233'
        }
        res = tf._update_publications(fake)
        self.assertNotIn('pubmed', res)
        self.assertEqual(res['publications'], ['PMID:1233'])

    def test_update_publications_function_if_pubmed_id_is_not_prefixed(self):
        tf = BaseTransformer(self._input)
        fake = {
            'pubmed': 1233
        }
        res = tf._update_publications(fake)
        self.assertNotIn('pubmed', res)
        self.assertEqual(res['publications'], ['PMID:1233'])

    def test_update_publications_function_if_pmc_id_is_prefixed(self):
        tf = BaseTransformer(self._input)
        fake = {
            'pmc': 'PMC:1233'
        }
        res = tf._update_publications(fake)
        self.assertNotIn('pmc', res)
        self.assertEqual(res['publications'], ['PMC:1233'])

    def test_update_publications_function_if_pmc_id_is_not_prefixed(self):
        tf = BaseTransformer(self._input)
        fake = {
            'pmc': 123
        }
        res = tf._update_publications(fake)
        self.assertNotIn('pmc', res)
        self.assertEqual(res['publications'], ['PMC:123'])

    def test_extract_output_ids_function_if_output_id_type_not_in_result(self):
        tf = BaseTransformer(self._input)
        fake = {
            'kk': 1
        }
        res = tf.extract_output_ids(fake)
        self.assertEqual(res, [])

    def test_extract_output_ids_function_if_output_id_type_is_in_result(self):
        tf = BaseTransformer(self._input)
        fake = {
            'DOID': 1
        }
        res = tf.extract_output_ids(fake)
        self.assertEqual(res, ['DOID:1'])

    def test_add_edge_info_function_if_result_is_empty(self):
        tf = BaseTransformer(self._input)
        fake = {}
        res = tf.add_edge_info('NCBIGene:1017', fake)
        self.assertEqual(res, [])
