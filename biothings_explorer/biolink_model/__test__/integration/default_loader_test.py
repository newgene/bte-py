import unittest
from biothings_explorer.biolink_model.loader.default_loader import DefaultLoader


class TestDefaultLoader(unittest.TestCase):
    def test_biolink_yaml_should_be_read_from_data(self):
        loader = DefaultLoader()
        res = loader.load()
        self.assertIn('id', res)
        self.assertEqual(res['id'], 'https://w3id.org/biolink/biolink-model')
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'Biolink-Model')
