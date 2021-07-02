import unittest
from biothings_explorer.trapi.biothings.controllers.association import association


class TestAssociationMode(unittest.TestCase):
    def test_by_default_should_return_all_associations(self):
        res = association()
        self.assertGreater(len(res), 10)
        self.assertIn('subject', res[0])
        self.assertIn('api', res[0])

    def test_if_sub_specified_should_only_return_associations_related_to_the_sub(self):
        res = association('Gene')
        input_types = set([item['subject'] for item in res])
        self.assertEqual(len(input_types), 1)
        self.assertEqual(list(input_types), ['Gene'])

    def test_if_invalid_sub_specified_should_only_empty_list(self):
        res = association('Gene1')
        self.assertEqual(res, [])

    def test_if_obj_specified_should_only_return_associations_related_to_the_obj(self):
        res = association(None, 'ChemicalSubstance')
        output_types = set([item['object'] for item in res])
        input_types = set([item['subject'] for item in res])
        self.assertGreater(len(input_types), 1)
        self.assertEqual(len(output_types), 1)
        self.assertEqual(list(output_types), ['ChemicalSubstance'])

    def test_if_pred_specified_should_only_return_associations_related_to_the_pred(self):
        res = association(None, None, 'treats')
        preds = set([item['predicate'] for item in res])
        input_types = set([item['subject'] for item in res])
        self.assertGreater(len(input_types), 1)
        self.assertEqual(len(preds), 1)
        self.assertEqual(list(preds), ['treats'])

    def test_if_api_specified_should_return_associations_related_to_the_name(self):
        res = association(None, None, None, 'MyGene.info API')
        apis = set([item['api']['name'] for item in res])
        input_types = set([item['subject'] for item in res])
        self.assertGreater(len(input_types), 1)
        self.assertEqual(len(apis), 1)
        self.assertEqual(list(apis), ['MyGene.info API'])

    def test_if_source_specified_should_only_return_associations_related_to_the_source(self):
        res = association(None, None, None, None, 'drugbank')
        sources = set([item['provided_by'] for item in res])
        input_types = set([item['subject'] for item in res])
        self.assertGreater(len(input_types), 1)
        self.assertEqual(len(sources), 1)
        self.assertEqual(list(sources), ['drugbank'])

    def test_if_both_sub_and_obj_specified_should_only_return_associations_related_to_both_sub_and_obj(self):
        res = association('Gene', 'ChemicalSubstance')
        output_types = set([item['object'] for item in res])
        input_types = set([item['subject'] for item in res])
        self.assertEqual(len(input_types), 1)
        self.assertEqual(len(output_types), 1)
        self.assertEqual(list(input_types), ['Gene'])
        self.assertEqual(list(output_types), ['ChemicalSubstance'])
