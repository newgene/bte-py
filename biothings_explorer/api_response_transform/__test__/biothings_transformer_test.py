import os
import unittest
import json
from biothings_explorer.api_response_transform.transformers.biothings_transformer import BioThingsTransformer


class TestBiothingsTransformerForPostQuery(unittest.TestCase):

    def setUp(self):
        post_query_response_path =  os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'biothings', 'mychem_post.json'))
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'biothings', 'mychem_example_edge.json'))
        with open(post_query_response_path) as f1, open(edge_path) as f2:
            self.response = json.load(f1)
            edge = json.load(f2)
            self._input = {
                'response': self.response,
                'edge': edge,
            }

    def test_biothings_wrapper(self):
        tf = BioThingsTransformer(self._input)
        res = tf.pair_input_with_api_response()
        self.assertEqual(len(res), 2)
        self.assertIn('DRUGBANK:DB00188', res)
        self.assertEqual(len(res['DRUGBANK:DB00188']), 2)
        self.assertNotIn('DRUGBANK:DB0000', res)


class TestBiothingsTransformerForPostQueryUsingMygene(unittest.TestCase):

    def setUp(self):
        post_query_response_path =  os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'biothings', 'mygene_post.json'))
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'biothings', 'mygene_example_edge.json'))
        with open(post_query_response_path) as f1, open(edge_path) as f2:
            self.response = json.load(f1)
            edge = json.load(f2)
            self._input = {
                'response': self.response,
                'edge': edge,
            }

    def test_biothings_wrapper(self):
        tf = BioThingsTransformer(self._input)
        res = tf.pair_input_with_api_response()
        self.assertEqual(len(res), 1)
        self.assertIn('NCBIGene:1017', res)
        self.assertEqual(len(res['NCBIGene:1017']), 1)

    def test_biothings_transform(self):
        tf = BioThingsTransformer(self._input)
        res = tf.transform()
        self.assertEqual(len(res), 27)
        self.assertNotIn('pubmed', res[0])
        self.assertIn('publications', res[0])
        self.assertEqual(res[0]['publications'], ["PMID:21873635"])


class TestBiothingsTransformerForGetQuery(unittest.TestCase):

    def setUp(self):
        post_query_response_path =  os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'biothings', 'drug_response_get_response.json'))
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'biothings', 'drug_response_example_edge.json'))
        with open(post_query_response_path) as f1, open(edge_path) as f2:
            self.response = json.load(f1)
            edge = json.load(f2)
            self._input = {
                'response': self.response,
                'edge': edge,
            }

    def test_biothings_wrapper(self):
        tf = BioThingsTransformer(self._input)
        res = tf.pair_input_with_api_response()
        self.assertEqual(len(res), 1)
        self.assertIn('PUBCHEM:11373846', res)
        self.assertEqual(len(res['PUBCHEM:11373846']), 1)
