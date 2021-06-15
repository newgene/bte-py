import unittest
from biothings_explorer.bte_trapi_query_graph_handler.utils import remove_biolink_prefix, to_array, get_unique


class TestUtilityFunctions(unittest.TestCase):
    def test_remove_biolink_prefix_string_input_with_biolink_prefix_should_be_removed(self):
        _input = 'biolink:treats'
        res = remove_biolink_prefix(_input)
        self.assertEqual(res, 'treats')

    def test_string_input_without_biolink_prefix_should_be_kept_same(self):
        _input = 'treats'
        res = remove_biolink_prefix(_input)
        self.assertEqual(res, 'treats')

    def test_to_array_array_input_should_return_itself(self):
        _input = ['a']
        res = to_array(_input)
        self.assertEqual(res, ['a'])

    def test_to_array_non_array_input_should_return_an_array_of_one_element_being_itself(self):
        _input = 'a'
        res = to_array(_input)
        self.assertEqual(res, ['a'])