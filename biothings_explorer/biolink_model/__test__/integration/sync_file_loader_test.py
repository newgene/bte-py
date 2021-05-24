import os
import unittest
from biothings_explorer.biolink_model.loader.sync_loader_factory import SyncFileLoader


class TestFileLoader(unittest.TestCase):
    def test_biolink_yaml_should_be_read_from_file_path(self):
        loader = SyncFileLoader()
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        res = loader.load(file_path)
        self.assertIn('id', res)
        self.assertEqual(res['id'], 'https://w3id.org/biolink/biolink-model')
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'Biolink-Model')
