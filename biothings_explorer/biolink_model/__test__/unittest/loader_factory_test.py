import os
import unittest
from biothings_explorer.biolink_model.loader.url_loader import URLLoader
from biothings_explorer.biolink_model.loader.file_loader import FileLoader
from biothings_explorer.biolink_model.loader.default_loader import DefaultLoader
from biothings_explorer.biolink_model.loader.loader_factory import loader


class TestLoaderEntryPoint(unittest.TestCase):
    def test_when_input_is_undefined_return_default_loader(self):
        res = loader()
        self.assertIsInstance(res, DefaultLoader)

    def test_when_input_is_url_return_url_loader(self):
        res = loader('http://123')
        self.assertIsInstance(res, URLLoader)
        res1 = loader('https://123')
        self.assertIsInstance(res1, URLLoader)

    def test_when_input_is_a_valid_path_return_path_loader(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))

        res = loader(file_path)
        self.assertIsInstance(res, FileLoader)

    def test_when_input_is_invalid_path_raise_exception(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink1.yaml'))
        with self.assertRaises(Exception):
            loader(file_path)
