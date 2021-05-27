import unittest
from biothings_explorer.biomedical_id_resolver.validate.biolink_based_validator import BioLinkBasedValidator


class IntegrationTestForBioLinkBasedValidator(unittest.TestCase):
    def test_semantic_type_and_prefix_defined_in_biolink_and_config_should_appear_in_resolvable(self):
        _input = {
            'Disease': ["MONDO:1234"]
        }

        validator = BioLinkBasedValidator(_input)
        validator.validate()
        self.assertIn('Disease', validator.resolvable)
        self.assertEqual(validator.resolvable['Disease'], ["MONDO:1234"])
        self.assertEqual(validator.irresolvable, {})

    def test_semantic_type_but_not_prefix_defined_in_biolink_and_config_should_appear_in_irresolvable(self):
        _input = {
            'Disease': ["MONDO1:1234"]
        }

        validator = BioLinkBasedValidator(_input)
        validator.validate()
        self.assertIn('Disease', validator.irresolvable)
        self.assertEqual(validator.irresolvable['Disease'], ["MONDO1:1234"])
        self.assertEqual(validator.resolvable, {})

    def test_semantic_type_but_not_prefix_defined_in_biolink_and_config_should_appear_in_irresolvable(self):
        _input = {
            "GeneOrGeneProduct": ["CHEMBL.TARGET:CHEBML123"]
        }

        validator = BioLinkBasedValidator(_input)
        validator.validate()
        self.assertIn('GeneOrGeneProduct', validator.irresolvable)
        self.assertEqual(validator.irresolvable['GeneOrGeneProduct'], ["CHEMBL.TARGET:CHEBML123"])
        self.assertNotIn('Gene', validator.irresolvable)
        self.assertEqual(validator.resolvable, {})

    def test_semantic_type_and_prefix_that_is_not_defined_in_biolink_or_config_should_appear_in_irresolvable(self):
        _input = {
            'Disease1': ["MONDO:1234"]
        }

        validator = BioLinkBasedValidator(_input)
        validator.validate()
        self.assertIn('Disease1', validator.irresolvable)
        self.assertEqual(validator.irresolvable['Disease1'], ["MONDO:1234"])
        self.assertEqual(validator.resolvable, {})

    def test_descendant_semantic_type_and_prefix_defined_in_biolink_and_config_should_appear_in_resolvable(self):
        _input = {
            'DiseaseOrPhenotypicFeature': ["UMLS:1234"]
        }

        validator = BioLinkBasedValidator(_input)
        validator.validate()
        self.assertIn('Disease', validator.resolvable)
        self.assertEqual(validator.resolvable['Disease'], ["UMLS:1234"])
        self.assertIn('PhenotypicFeature', validator.resolvable)
        self.assertEqual(validator.resolvable['PhenotypicFeature'], ["UMLS:1234"])
        self.assertEqual(validator.irresolvable, {})

    def test_descendant_semantic_type_and_prefix_in_biolink_should_appear_in_resolvable_using_namedthing(self):
        _input = {
            "NamedThing": ["UMLS:1234"]
        }

        validator = BioLinkBasedValidator(_input)
        validator.validate()
        self.assertIn('Disease', validator.resolvable)
        self.assertEqual(validator.resolvable['Disease'], ["UMLS:1234"])
        self.assertIn('PhenotypicFeature', validator.resolvable)
        self.assertEqual(validator.resolvable['PhenotypicFeature'], ["UMLS:1234"])
        self.assertIn('AnatomicalEntity', validator.resolvable)
        self.assertEqual(validator.resolvable['AnatomicalEntity'], ["UMLS:1234"])
        self.assertIn('Cell', validator.irresolvable)
        self.assertEqual(validator.irresolvable['Cell'], ["UMLS:1234"])
        self.assertIn('CellularComponent', validator.irresolvable)
        self.assertEqual(validator.irresolvable['CellularComponent'], ["UMLS:1234"])

    def test_descendant_semantic_type_but_not_prefix_defined_in_biolink_and_config_should_appear_in_irresolvable(self):
        _input = {
            'NamedThing': ['KEGG.GENE:1234']
        }

        validator = BioLinkBasedValidator(_input)
        validator.validate()
        self.assertEqual(validator.resolvable, {})
        self.assertIn('Gene', validator.irresolvable)
        self.assertEqual(validator.irresolvable['Gene'], ['KEGG.GENE:1234'])
        self.assertIn('NamedThing', validator.irresolvable)
        self.assertEqual(validator.irresolvable['NamedThing'], ['KEGG.GENE:1234'])

    def test_item_with_comma_in_it_should_be_counted_as_irresolvable(self):
        _input = {
            'ChemicalSubstance': ["KEGG:1,2"]
        }

        validator = BioLinkBasedValidator(_input)
        validator.validate()
        self.assertEqual(validator.resolvable, {})
        self.assertIn('ChemicalSubstance', validator.irresolvable)
        self.assertEqual(validator.irresolvable['ChemicalSubstance'], ["KEGG:1,2"])
