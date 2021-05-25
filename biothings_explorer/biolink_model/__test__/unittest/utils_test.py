import unittest
from biothings_explorer.biolink_model.utils import underscore


class TestUtilsModule(unittest.TestCase):
    def test_underscore_should_return_affects_abundance_of(self):
        res = underscore('affects abundance of')
        self.assertEqual(res, 'affects_abundance_of')

    def test_underscore_should_return_regulates_process_to_process(self):
        res = underscore('regulates, process to process')
        self.assertEqual(res, 'regulates_process_to_process')

    def test_underscore_should_return_undefined(self):
        res = underscore(None)
        self.assertIsNone(res)
