import unittest
from biothings_explorer.biomedical_id_resolver.resolve.biolink_based_resolver import BioLinkBasedResolver
from biothings_explorer.biomedical_id_resolver.bioentity.valid_bioentity import ResolvableBioEntity
from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity


class TestIdResolver(unittest.TestCase):
    def test_valid_inputs_should_be_correctly_resolved(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'Gene': ["NCBIGene:1017"]})
        self.assertIn('NCBIGene:1017', res)
        self.assertEqual(len(res['NCBIGene:1017']), 1)
        self.assertIsInstance(res['NCBIGene:1017'][0], ResolvableBioEntity)
        self.assertEqual(res['NCBIGene:1017'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0].label, 'CDK2')

    def test_biothings_output_include_integer_should_ne_converted_to_string(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'ChemicalSubstance': ["CHEMBL.COMPOUND:CHEMBL744"]})
        self.assertIsInstance(res['CHEMBL.COMPOUND:CHEMBL744'][0], ResolvableBioEntity)
        self.assertEqual(res['CHEMBL.COMPOUND:CHEMBL744'][0].db_ids['PUBCHEM.COMPOUND'], ['5070'])

    def test_valid_inputs_from_multiple_semantic_types_should_be_correctly_resolved(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'Gene': ["NCBIGene:1017"], "ChemicalSubstance": ["DRUGBANK:DB01609"]})
        self.assertIn('NCBIGene:1017', res)
        self.assertEqual(len(res['NCBIGene:1017']), 1)
        self.assertIsInstance(res['NCBIGene:1017'][0], ResolvableBioEntity)
        self.assertEqual(res['NCBIGene:1017'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0].label, 'CDK2')
        self.assertIn('DRUGBANK:DB01609', res)
        self.assertEqual(len(res['DRUGBANK:DB01609']), 1)
        self.assertIsInstance(res['DRUGBANK:DB01609'][0], ResolvableBioEntity)
        self.assertEqual(res['DRUGBANK:DB01609'][0].label.upper(), 'DEFERASIROX')

