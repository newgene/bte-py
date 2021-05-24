import unittest
import os
from biothings_explorer.biolink_model.loader.file_loader import FileLoader


class TestFileLoader(unittest.TestCase):
    def test_biolink_yaml_should_be_read_from_data(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        loader = FileLoader()
        res = loader.load(file_path)
        self.assertIn('id', res)
        self.assertEqual(res['id'], 'https://w3id.org/biolink/biolink-model')
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'Biolink-Model')
