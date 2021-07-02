import unittest
from biothings_explorer.trapi.biothings.controllers.utils import remove_bio_link_prefix
from biothings_explorer.trapi.utils.common import remove_quotes_from_query


class TestUtils(unittest.TestCase):
    def test_remove_quotes_from_query_single_quotes_should_be_removed(self):
        _input = "'kevin'"
        res = remove_quotes_from_query(_input)
        self.assertEqual(res, 'kevin')

    def test_double_quotes_should_be_removed(self):
        _input = '"kevin"'
        res = remove_quotes_from_query(_input)
        self.assertEqual(res, 'kevin')

    def test_unquoted_string_should_return_itself(self):
        _input = 'kevin'
        res = remove_quotes_from_query(_input)
        self.assertEqual(res, 'kevin')

    def test_string_with_only_quotes_in_the_middle_should_also_return_itself(self):
        _input = 'ke"vin'
        res = remove_quotes_from_query(_input)
        self.assertEqual(res, 'ke"vin')
