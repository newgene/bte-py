import unittest
from biothings_explorer.biomedical_id_resolver.validate.default_validator import DefaultValidator


class TestValidatorClass(unittest.TestCase):
    def test_semantic_types_not_appear_in_apimeta_file_should_be_classified_as_irresolvable(self):
        test_data = { "Gene": ["NCBIGene:1017"], "Gene1": ["NCBIGene:1018"] }
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('Gene1', vd.irresolvable)

    def test_if_prefixes_not_appear_in_apimeta_file_should_be_classified_as_irresolvable(self):
        test_data = { "Gene": ["NCBIGene:1017", "kkk:1323"] }
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('Gene', vd.irresolvable)
        self.assertIn('kkk:1323', vd.irresolvable['Gene'])

    def test_check_if_irresolvable_object_are_correctly_initialized(self):
        test_data = {"Gene": ["NCBIGene:1017", "kkk:1323", "kkk:12345"]}
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('Gene', vd.irresolvable)
        self.assertIn('kkk:1323', vd.irresolvable['Gene'])
        self.assertIn('kkk:12345', vd.irresolvable['Gene'])

    #TODO FAILS
    def test_id_appear_in_config_should_be_mapped_to_the_correct_semantic_type(self):
        test_data = {"undefined": ["NCBIGene:1017", "kkk:1323"]}
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('NCBIGene:1017', vd.resolvable['Gene'])
        self.assertIn('NCBIGene:1017', vd.irresolvable['undefined'])
        self.assertIn('kkk:1323', vd.irresolvable['undefined'])

    # TODO FAILS
    def test_id_that_can_be_mapped_to_multiple_semantic_types_are_correctly_mapped(self):
        test_data = {"undefined": ["NCBIGene:1017", "OMIM:123"]}
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('OMIM:123', vd.resolvable['Gene'])
        self.assertIn('OMIM:123', vd.resolvable['Disease'])

    def test_valid_answers_can_be_retrieved_through_valid_property_of_the_class(self):
        test_data = {"Gene": ["NCBIGene:1017", "kkk:1323"], "ChemicalSubstance": ["DRUGBANK:DB0001"]}
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('Gene', vd.resolvable)
        self.assertEqual(vd.resolvable['Gene'], ['NCBIGene:1017'])
        self.assertIn('ChemicalSubstance', vd.resolvable)
        self.assertEqual(vd.resolvable['ChemicalSubstance'], ["DRUGBANK:DB0001"])