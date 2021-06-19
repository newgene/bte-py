import unittest
from biothings_explorer.bte_trapi_query_graph_handler.biolink import BioLinkModelInstance


class TestBioLinkModelClass(unittest.TestCase):
    def test_reverse_with_correct_predicate(self):
        res = BioLinkModelInstance.reverse('treats')
        self.assertEqual(res, 'treated_by')

    def test_reverse_with_correct_predicate_if_it_contains_underscore(self):
        res = BioLinkModelInstance.reverse('treated_by')
        self.assertEqual(res, 'treats')

    def test_reverse_with_predicate_having_symmetric_equal_to_true(self):
        res = BioLinkModelInstance.reverse('correlated_with')
        self.assertEqual(res, 'correlated_with')

    def test_predicate_with_no_inverse_property_and_symmetric_not_equal_to_true(self):
        res = BioLinkModelInstance.reverse('has_phenotype')
        self.assertEqual(res, 'phenotype_of')

    def test_predicate_not_exist_in_biolink_model(self):
        res = BioLinkModelInstance.reverse('haha')
        self.assertIsNone(res)

    def test_if_input_not_string_return_none(self):
        res = BioLinkModelInstance.reverse(['dd'])
        self.assertIsNone(res)

    def test_get_descendants_if_input_is_in_biolink_model_return_all_its_descendants_and_itself(self):
        res = BioLinkModelInstance.get_descendant_classes('MolecularEntity')
        self.assertIn('Drug', res)
        self.assertIn('Gene', res)
        self.assertIn('MolecularEntity', res)

    def test_if_input_is_in_biolink_model_but_doesnt_have_descendants_return_itself(self):
        res = BioLinkModelInstance.get_descendant_classes('Gene')
        self.assertEqual(res, ['Gene'])

    def test_if_input_is_not_in_biolink_return_itself(self):
        res = BioLinkModelInstance.get_descendant_classes('Gene1')
        self.assertEqual(res, 'Gene1')

    def test_get_descendant_predicates_if_input_is_in_biolink_model_return_all_its_descendants_and_itself(self):
        res = BioLinkModelInstance.get_descendant_predicates('related_to')
        self.assertIn('subclass_of', res)
        self.assertIn('superclass_of', res)
        self.assertIn('related_to', res)