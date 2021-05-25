import unittest
import os
from biothings_explorer.biolink_model.loader.sync_file_loader import SyncFileLoader
from biothings_explorer.biolink_model.loader.sync_default_loader import SyncDefaultLoader
from biothings_explorer.biolink_model.loader.sync_loader_factory import sync_loader


class TestLoaderEntryPoint(unittest.TestCase):
    def test_when_input_is_undefined_return_sync_default_loader(self):
        res = sync_loader()
        self.assertIsInstance(res, SyncDefaultLoader)

    def test_when_input_is_a_valid_path_return_sync_file_loader(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        res = sync_loader(file_path)
        self.assertIsInstance(res, SyncFileLoader)
