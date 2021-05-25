import unittest
from biothings_explorer.biolink_model.loader.url_loader import URLLoader


class TestURLLoader(unittest.TestCase):
    def test_biolink_yaml_should_be_read_from_data(self):
        loader = URLLoader()
        res = loader.load('https://raw.githubusercontent.com/biolink/biolink-model/master/biolink-model.yaml')
        self.assertIn('id', res)
        self.assertEqual(res['id'], 'https://w3id.org/biolink/biolink-model')
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'Biolink-Model')
