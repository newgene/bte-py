import unittest
from biothings_explorer.biomedical_id_resolver.utils import (
    generate_curie,
    get_prefix_from_curie,
    generate_object_with_no_duplicate_elements_in_value,
    append_array_or_non_array_object_to_array,
    generate_db_id,
    generate_id_type_dict
)


class TestUtilsModule(unittest.TestCase):
    def test_id_that_is_always_a_curie_should_return_itself(self):
        input_id = 'MONDO:000123'
        res = generate_curie('MONDO', input_id)
        self.assertEqual(res, input_id)

    def test_id_that_is_not_always_a_curie_should_return_prefix_plus_colon_and_itself(self):
        input_id = '1017'
        res = generate_curie('NCBIGene', input_id)
        self.assertEqual(res, 'NCBIGene:1017')

    def test_id_that_is_irresolvable_should_return_prefix_plus_color_and_itself(self):
        input_id = '1017'
        res = generate_curie('NCBIGene1', input_id)
        self.assertEqual(res, 'NCBIGene1:1017')

    def test_prefix_part_is_parsed_if_its_a_curie(self):
        input_id = 'MONDO:000123'
        res = get_prefix_from_curie(input_id)
        self.assertEqual(res, 'MONDO')

    def test_return_itself_if_input_is_not_a_curie(self):
        input_id = '1017'
        res = get_prefix_from_curie(input_id)
        self.assertEqual(res, input_id)

    def test_append_as_a_whole_if_input_is_not_array(self):
        _input = 'MONDO:000123'
        lst = ['123']
        res = append_array_or_non_array_object_to_array(lst, _input)
        self.assertEqual(len(res), 2)
        self.assertEqual(res, ['123', 'MONDO:000123'])

    def test_append_each_item_if_input_is_an_array(self):
        _input = ['MONDO:000123', 'MONDO:000124']
        lst = ['123']
        res = append_array_or_non_array_object_to_array(lst, _input)
        self.assertEqual(len(res), 3)
        self.assertEqual(res, ['123', 'MONDO:000123', 'MONDO:000124'])

    def test_convert_element_of_input_to_string_if_any_of_the_element_in_input_is_a_number(self):
        _input = ['MONDO:000123', 1017, 1018.1]
        lst = ['123']
        res = append_array_or_non_array_object_to_array(lst, _input)
        self.assertEqual(len(res), 4)
        self.assertEqual(res, ['123', 'MONDO:000123', '1017', '1018.1'])

    def test_convert_item_to_string_if_item_is_number(self):
        _input = 1017
        lst = ['123']
        res = append_array_or_non_array_object_to_array(lst, _input)
        self.assertEqual(len(res), 2)
        self.assertEqual(res, ['123', '1017'])

    def test_if_element_in_input_is_not_string_or_number_it_should_not_be_pushed(self):
        _input = ['MONDO:123', ['a', 'b']]
        lst = ['123']
        res = append_array_or_non_array_object_to_array(lst, _input)
        self.assertEqual(len(res), 2)
        self.assertEqual(res, ['123', 'MONDO:123'])

    def test_if_input_is_string_or_array_it_should_not_be_pushed(self):
        _input = {'a': 'b'}
        lst = ['123']
        res = append_array_or_non_array_object_to_array(lst, _input)
        self.assertEqual(len(res), 1)
        self.assertEqual(res, ['123'])

    def test_duplicate_items_are_removed_in_object_values(self):
        _input = {
            'item': ["123", "123", "345"]
        }

        self.assertEqual(len(_input['item']), 3)
        res = generate_object_with_no_duplicate_elements_in_value(_input)
        self.assertEqual(len(res['item']), 2)
        #TODO Items are flipped to work
        self.assertEqual(res['item'], ['123', '345'])

    def test_id_which_is_default_curie_should_return_itself(self):
        _input = 'MONDO:000123'
        res = generate_db_id(_input)
        self.assertEqual(res, _input)

    def test_id_which_is_not_default_curie_should_return_prefixed_removed_version(self):
        _input = 'NCBIGene:1017'
        res = generate_db_id(_input)
        self.assertEqual(res, '1017')

    def test_id_which_is_not_valid_but_has_curie_should_return_prefixed_removed_version(self):
        _input = 'NCBIGene1:1017'
        res = generate_db_id(_input)
        self.assertEqual(res, '1017')

    def test_id_which_is_not_valid_and_is_not_curie_should_return_itself(self):
        _input = '1017'
        res = generate_db_id(_input)
        self.assertEqual(res, '1017')

    def test_id_with_multiple_colons_in_it_should_only_trim_the_chars_before_the_first_occurrence_of_colon(self):
        _input = 'WIKIPATHWAYS:pathway:1017'
        res = generate_db_id(_input)
        self.assertEqual(res, 'pathway:1017')

    def test_generate_id_type_dict(self):
        res = generate_id_type_dict()
        self.assertIn('NCBIGene', res)
        self.assertEqual(res['NCBIGene'], ['Gene'])
        self.assertIn('OMIM', res)
        self.assertEqual(res['OMIM'], ['Gene', 'Disease'])