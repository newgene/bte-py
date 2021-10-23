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
        res = resolver.resolve({'SmallMolecule': ["CHEMBL.COMPOUND:CHEMBL744"]})
        self.assertIsInstance(res['CHEMBL.COMPOUND:CHEMBL744'][0], ResolvableBioEntity)
        self.assertEqual(res['CHEMBL.COMPOUND:CHEMBL744'][0].db_ids['PUBCHEM.COMPOUND'], ['5070'])

    def test_valid_inputs_from_multiple_semantic_types_should_be_correctly_resolved(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'Gene': ["NCBIGene:1017"], "SmallMolecule": ["DRUGBANK:DB01609"]})
        self.assertIn('NCBIGene:1017', res)
        self.assertEqual(len(res['NCBIGene:1017']), 1)
        self.assertIsInstance(res['NCBIGene:1017'][0], ResolvableBioEntity)
        self.assertEqual(res['NCBIGene:1017'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0].label, 'CDK2')
        self.assertIn('DRUGBANK:DB01609', res)
        self.assertEqual(len(res['DRUGBANK:DB01609']), 1)
        self.assertIsInstance(res['DRUGBANK:DB01609'][0], ResolvableBioEntity)
        self.assertEqual(res['DRUGBANK:DB01609'][0].label.upper(), 'DEFERASIROX')

    def test_irresolvable_inputs_should_be_part_of_the_result(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'Gene': ["NCBIGene:1017", "kkk:123"]})
        self.assertIn('kkk:123', res)
        self.assertEqual(len(res['kkk:123']), 1)
        self.assertIsInstance(res['kkk:123'][0], IrresolvableBioEntity)
        self.assertEqual(res['kkk:123'][0].primary_id, 'kkk:123')
        self.assertEqual(res['kkk:123'][0].label, 'kkk:123')

    def test_large_batch_of_inputs_should_be_correctly_resolved(self):
        fake_ncbi_gene_inputs = ['NCBIGene:' + str(item) for item in list(range(1990))]
        fake_omim_gene_inputs = ['OMIM:' + str(item) for item in list(range(2300))]
        fake_drug_bank_inputs = ['DRUGBANK:DB00' + str(item) for item in list(range(3500))]
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({
            'Gene': [*fake_ncbi_gene_inputs, *fake_omim_gene_inputs],
            'SmallMolecule': fake_drug_bank_inputs
        })
        self.assertEqual(len(res.keys()), len(fake_drug_bank_inputs) + len(fake_omim_gene_inputs) +
                         len(fake_ncbi_gene_inputs))
        self.assertIsInstance(res['OMIM:0'][0], IrresolvableBioEntity)

    def test_inputs_with_namedthing_semantic_type_should_be_correctly_resolved(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'NamedThing': ['NCBIGene:1017']})
        self.assertIn('NCBIGene:1017', res)
        self.assertEqual(len(res['NCBIGene:1017']), 2)
        self.assertIsInstance(res['NCBIGene:1017'][0], ResolvableBioEntity)
        self.assertEqual(res['NCBIGene:1017'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0].label, 'CDK2')
        self.assertEqual(res['NCBIGene:1017'][0].semantic_type, 'Gene')
        self.assertIn('NamedThing', res['NCBIGene:1017'][0].semantic_types)

    def test_inputs_with_namedthing_semantic_type_and_could_be_mapped_to_multiple_semantic_types(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'NamedThing': ['UMLS:C0008780']})
        self.assertIn('UMLS:C0008780', res)
        valid = [rec for rec in res['UMLS:C0008780'] if isinstance(rec, ResolvableBioEntity)]
        valid_types = [item.semantic_type for item in valid]
        self.assertIn('PhenotypicFeature', valid_types)
        self.assertIn('Disease', valid_types)
        self.assertEqual(len(valid), 2)
        self.assertIn('NamedThing', valid[0].semantic_types)

    def test_inputs_with_namedthing_semantic_type_and_could_be_mapped_to_multiple_semantic_types_using_OMIMID(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'NamedThing': ['OMIM:116953']})
        self.assertIn('OMIM:116953', res)
        valid = [item for item in res['OMIM:116953'] if isinstance(item, ResolvableBioEntity)]
        self.assertEqual(len(valid), 1)
        self.assertIsInstance(valid[0], ResolvableBioEntity)
        self.assertEqual('NCBIGene:1017', valid[0].primary_id)
        self.assertEqual('CDK2', valid[0].label)
        self.assertEqual('Gene', valid[0].semantic_type)
        self.assertIn('NamedThing', valid[0].semantic_types)
        self.assertIn('BiologicalEntity', valid[0].semantic_types)

    def test_inputs_with_undefined_semantic_type_and_could_not_be_mapped_to_any_semantic_type_return_irresolvable(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'undefined': ['OMIM1:116953']})
        self.assertIn('OMIM1:116953', res)
        self.assertIsInstance(res['OMIM1:116953'][0], IrresolvableBioEntity)
        self.assertEqual(res['OMIM1:116953'][0].semantic_type, 'undefined')

    def test_irresolvable_inputs_should_not_overwrite_the_result_of_a_valid_input(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'Gene': ['NCBIGene:1017'], 'Disease': ['NCBIGene:1017']})
        self.assertIn('NCBIGene:1017', res)
        self.assertEqual(len(res['NCBIGene:1017']), 2)
        self.assertIsInstance(res['NCBIGene:1017'][0], ResolvableBioEntity)
        self.assertEqual(res['NCBIGene:1017'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0].label, 'CDK2')
        self.assertIsInstance(res['NCBIGene:1017'][1], IrresolvableBioEntity)

    def test_input_with_space_in_it_should_be_correctly_resolved(self):
        resolver = BioLinkBasedResolver()
        res = resolver.resolve({'SmallMolecule': ["name:Regorafenib", "name:Sunitinib", "name:Imatinib", "name:Ponatinib", "name:Dasatinib", "name:Bosutinib", "name:Imatinib Mesylate"]})
        self.assertIn('name:Imatinib Mesylate', res)
        self.assertIn('name:Regorafenib', res)
        self.assertEqual(len(res['name:Imatinib Mesylate']), 1)
        self.assertIsInstance(res['name:Imatinib Mesylate'][0], ResolvableBioEntity)