import unittest
from biothings_explorer.biomedical_id_resolver.validate.default_validator import DefaultValidator
from biothings_explorer.biomedical_id_resolver.common.exceptions import IrresolvableIDResolverInputError


class TestValidatorClass(unittest.TestCase):
    def test_exception_if_input_is_an_array(self):
        test_data = ['123']
        vd = DefaultValidator(test_data)
        with self.assertRaises(IrresolvableIDResolverInputError):
            vd.validate()

        with self.assertRaisesRegex(IrresolvableIDResolverInputError, 'Your Input to ID Resolver is Irresolvable. It should be a plain object!'):
            vd.validate()

    def test_exception_if_input_is_a_string(self):
        test_data = '123'
        vd = DefaultValidator(test_data)
        with self.assertRaises(IrresolvableIDResolverInputError):
            vd.validate()

        with self.assertRaisesRegex(IrresolvableIDResolverInputError, 'Your Input to ID Resolver is Irresolvable. It should be a plain object!'):
            vd.validate()

    def test_not_raise_exception_if_input_is_an_object(self):
        test_data = {}
        try:
            vd = DefaultValidator(test_data)
            vd.validate()
        except IrresolvableIDResolverInputError:
            self.fail('Exception raised')

    def test_raise_exception_if_input_is_values_of_input_is_string(self):
        test_data = {'Gene': '123'}
        vd = DefaultValidator(test_data)
        with self.assertRaises(IrresolvableIDResolverInputError):
            vd.validate()

        with self.assertRaisesRegex(IrresolvableIDResolverInputError, 'Your Input to ID Resolver is Irresolvable. All values of your input dictionary should be a list!'):
            vd.validate()

    def test_raise_exception_if_input_is_values_of_input_is_an_object(self):
        test_data = {'Gene': {'Protein': ['PR:001']}}
        vd = DefaultValidator(test_data)

        with self.assertRaises(IrresolvableIDResolverInputError):
            vd.validate()

        with self.assertRaisesRegex(IrresolvableIDResolverInputError, 'Your Input to ID Resolver is Irresolvable. All values of your input dictionary should be a list!'):
            vd.validate()

    def test_not_raise_exception_if_values_of_input_is_array(self):
        test_data = {'Gene': ['NCBIGene:1017']}
        try:
            vd = DefaultValidator(test_data)
            vd.validate()
        except IrresolvableIDResolverInputError:
            self.fail('Exception raised')

    def test_raise_exception_if_values_of_input_contains_non_string_type(self):
        test_data = {'Gene': [123]}
        vd = DefaultValidator(test_data)

        with self.assertRaises(IrresolvableIDResolverInputError):
            vd.validate()

        with self.assertRaisesRegex(IrresolvableIDResolverInputError, 'Your Input to ID Resolver is Irresolvable. Each item in the values of your input dictionary should be a curie. Spotted 123 is not a curie'):
            vd.validate()

    def test_raise_exception_if_values_of_input_contains_non_curie_type(self):
        test_data = {'Gene': ['1234']}
        vd = DefaultValidator(test_data)
        with self.assertRaises(IrresolvableIDResolverInputError):
            vd.validate()

        with self.assertRaisesRegex(IrresolvableIDResolverInputError, 'Your Input to ID Resolver is Irresolvable. Each item in the values of your input dictionary should be a curie. Spotted 1234 is not a curie'):
            vd.validate()

    def test_not_raise_exception_if_values_of_input_are_all_curies(self):
        test_data = {'Gene': ["NCBIGene:1234", "NCBIGene:1345"]}
        vd = DefaultValidator(test_data)
        try:
            vd.validate()
        except IrresolvableIDResolverInputError:
            self.fail('Exception raised')

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

    def test_id_appear_in_config_should_be_mapped_to_the_correct_semantic_type(self):
        test_data = {"undefined": ["NCBIGene:1017", "kkk:1323"]}
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('NCBIGene:1017', vd.resolvable['Gene'])
        self.assertNotIn('NCBIGene:1017', vd.irresolvable['undefined'])
        self.assertIn('kkk:1323', vd.irresolvable['undefined'])

    def test_id_that_can_be_mapped_to_multiple_semantic_types_are_correctly_mapped(self):
        test_data = {"undefined": ["NCBIGene:1017", "OMIM:123"]}
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('OMIM:123', vd.resolvable['Gene'])
        self.assertIn('OMIM:123', vd.resolvable['Disease'])

    def test_valid_answers_can_be_retrieved_through_valid_property_of_the_class(self):
        test_data = {"Gene": ["NCBIGene:1017", "kkk:1323"], "SmallMolecule": ["DRUGBANK:DB0001"]}
        vd = DefaultValidator(test_data)
        vd.validate()
        self.assertIn('Gene', vd.resolvable)
        self.assertEqual(vd.resolvable['Gene'], ['NCBIGene:1017'])
        self.assertIn('SmallMolecule', vd.resolvable)
        self.assertEqual(vd.resolvable['SmallMolecule'], ["DRUGBANK:DB0001"])
