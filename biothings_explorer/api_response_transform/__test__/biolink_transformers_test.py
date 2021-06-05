import os
import unittest
import json
from biothings_explorer.api_response_transform.transformers.biolink_transformer import BiolinkTransformer


class TestBiolinkTransformer(unittest.TestCase):
    def setUp(self):
        response_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'biolink', 'response.json'))
        edge_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'data', 'biolink', 'edge.json'))
        with open(response_path) as f1, open(edge_path) as f2:
            self.response = json.load(f1)
            edge = json.load(f2)
            self._input = {
                'response': self.response,
                'edge': edge,
            }

    def test_biolink_wrapper(self):
        tf = BiolinkTransformer(self._input)
        res = tf.wrap(self.response)
        self.assertEqual(res['associations'][0]['object']['HGNC'], '10956')
        self.assertEqual(res['associations'][0]['publications'][0]['id'], '21685912')
        self.assertNotIn('publications', res['associations'][1])
        self.assertNotIn('provided_by', res['associations'][1])

    def test_biolink_wrapper_if_not_association_field_as_root_key(self):
        tf = BiolinkTransformer(self._input)
        res = tf.wrap({'data': []})
        self.assertEqual({'data': []}, res)

    def test_biolink_wrapper_if_no_object_id_should_be_prefixed(self):
        tf = BiolinkTransformer(self._input)
        res = tf.wrap(
            {
                'associations': [
                    {
                        'object':{
                            'id': "MONDO:12345"
                        }
                    }
                ]
            }
        )
        self.assertEqual(res['associations'][0]['object']['MONDO'], "MONDO:12345")

    def test_biolink_wrapper_if_no_object_field_present(self):
        tf = BiolinkTransformer(self._input)
        fake_response = {
            'associations': [
                {
                    'object1': {
                        'id': "MONDO:12345"
                    }
                }
            ]
        }
        res = tf.wrap(fake_response)
        self.assertEqual(fake_response, res)

    def test_biolink_wrapper_if_no_object_id_field_present(self):
        tf = BiolinkTransformer(self._input)
        fake_response = {
            'associations': [
                {
                    'object': {
                        'id1': 'MONDO:12345'
                    }
                }
            ]
        }
        res = tf.wrap(fake_response)
        self.assertEqual(res, fake_response)

    def test_biolink_json_transform_function(self):
        tf = BiolinkTransformer(self._input)
        wrapped_response = tf.wrap(self.response)
        res = tf.json_transform(wrapped_response)
        self.assertIn('related_to', res)
        self.assertEqual(res['related_to'][0]['HGNC'], '10956')
        #TODO FAILS
        self.assertEqual(res['related_to'][0]['pubmed'][0], '21685912')
        self.assertEqual(res['related_to'][0]['relation'], 'contributes to condition')
        self.assertEqual(res['related_to'][0]['source'][0], 'https://archive.monarchinitiative.org/#gwascatalog')
        self.assertEqual(res['related_to'][0]['taxid'], 'NCBITaxon:9606')