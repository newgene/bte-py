import unittest
from biothings_explorer.biomedical_id_resolver.resolve.default_resolver import DefaultResolver
from biothings_explorer.biomedical_id_resolver.bioentity.valid_bioentity import ResolvableBioEntity
from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity


class TestIDResolver(unittest.TestCase):
    def test_valid_inputs_should_be_correctly_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Gene': ["NCBIGene:1017"]})
        self.assertIn('NCBIGene:1017', res)
        self.assertEqual(len(res['NCBIGene:1017']), 1)
        self.assertIsInstance(res['NCBIGene:1017'][0], ResolvableBioEntity)
        self.assertEqual(res['NCBIGene:1017'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0].label, 'CDK2')

    def test_sumbol_should_be_resolved_to_corresponding_human_gene(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Gene': ["SYMBOL:VAMP2"]})
        self.assertIn("SYMBOL:VAMP2", res)
        self.assertEqual(len(res["SYMBOL:VAMP2"]), 1)
        self.assertIsInstance(res["SYMBOL:VAMP2"][0], ResolvableBioEntity)
        self.assertEqual(res["SYMBOL:VAMP2"][0].primary_id, 'NCBIGene:6844')
        self.assertEqual(res["SYMBOL:VAMP2"][0].label, 'VAMP2')

    def test_lincs_id_should_be_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'SmallMolecule': ['LINCS:LSM-2471']})
        self.assertIn('LINCS:LSM-2471', res)
        self.assertEqual(len(res['LINCS:LSM-2471']), 1)
        self.assertIsInstance(res['LINCS:LSM-2471'][0], ResolvableBioEntity)
        self.assertEqual(res['LINCS:LSM-2471'][0].primary_id, 'PUBCHEM.COMPOUND:5070')
        self.assertEqual(res['LINCS:LSM-2471'][0].db_ids['LINCS'], ["LSM-2471"])

    def test_protein_uniprot_id_should_be_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Protein': ['UniProtKB:P24941']})
        self.assertIn('UniProtKB:P24941', res)
        self.assertEqual(len(res['UniProtKB:P24941']), 1)
        self.assertIsInstance(res['UniProtKB:P24941'][0], ResolvableBioEntity)
        self.assertEqual(res['UniProtKB:P24941'][0].primary_id, 'UniProtKB:P24941')
        self.assertIn('ENSP00000243067', res['UniProtKB:P24941'][0].db_ids['ENSEMBL'])

    def test_protein_ensembl_id_should_be_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Protein': ['ENSEMBL:ENSP00000243067']})
        self.assertIn('ENSEMBL:ENSP00000243067', res)
        self.assertEqual(len(res['ENSEMBL:ENSP00000243067']), 1)
        self.assertIsInstance(res['ENSEMBL:ENSP00000243067'][0], ResolvableBioEntity)
        self.assertEqual(res['ENSEMBL:ENSP00000243067'][0].primary_id, 'UniProtKB:P24941')
        self.assertIn('ENSP00000243067', res['ENSEMBL:ENSP00000243067'][0].db_ids['ENSEMBL'])

    def test_records_from_a_query_with_multiple_hits_should_all_be_collected(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Disease': ["OMIM:307030"]})
        self.assertIn('OMIM:307030', res)
        self.assertEqual(len(res['OMIM:307030']), 1)
        self.assertIsInstance(res['OMIM:307030'][0], ResolvableBioEntity)
        self.assertEqual(res['OMIM:307030'][0].primary_id, 'MONDO:0010613')
        self.assertIn('C0268418', res['OMIM:307030'][0].db_ids['UMLS'])
        self.assertIn('C0574108', res['OMIM:307030'][0].db_ids['UMLS'])

    def test_valid_inputs_should_be_correctly_resolved_using_disease_gard_id(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Disease': ['GARD:4206']})
        self.assertIn('GARD:4206', res)
        self.assertEqual(len(res['GARD:4206']), 1)
        self.assertIsInstance(res['GARD:4206'][0], ResolvableBioEntity)
        self.assertEqual(res['GARD:4206'][0].primary_id, 'MONDO:0015278')

    def test_biothings_output_include_integer_should_be_converted_to_string(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'SmallMolecule': ['CHEMBL.COMPOUND:CHEMBL744']})
        self.assertIsInstance(res['CHEMBL.COMPOUND:CHEMBL744'][0], ResolvableBioEntity)
        self.assertEqual(res['CHEMBL.COMPOUND:CHEMBL744'][0].db_ids['PUBCHEM.COMPOUND'], ["5070"])

    def test_valid_inputs_from_multiple_semantic_types_should_be_correctly_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Gene': ["NCBIGene:1017"], 'SmallMolecule': ["DRUGBANK:DB01609"]})
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
        resolver = DefaultResolver()
        res = resolver.resolve({'Gene': ["NCBIGene:1017", "kkk:123"]})
        self.assertIn('kkk:123', res)
        self.assertIsInstance(res['kkk:123'][0], IrresolvableBioEntity)
        self.assertEqual(res['kkk:123'][0].primary_id, 'kkk:123')
        self.assertEqual(res['kkk:123'][0].label, 'kkk:123')

    def test_large_batch_of_inputs_should_be_correctly_resolved(self):
        fake_ncbi_gene_inputs = ['NCBIGene:' + str(item) for item in list(range(1990))]
        fake_omim_gene_inputs = ['OMIM:' + str(item) for item in list(range(2300))]
        fake_drug_bank_inputs = ['DRUGBANK:DB00' + str(item) for item in list(range(3500))]

        resolver = DefaultResolver()
        res = resolver.resolve({
            'Gene': [*fake_ncbi_gene_inputs, *fake_omim_gene_inputs],
            'SmallMolecule': fake_drug_bank_inputs
        })
        self.assertEqual(len(res.keys()), len(fake_drug_bank_inputs) + len(fake_ncbi_gene_inputs) + len(fake_omim_gene_inputs))
        self.assertIsInstance(res['OMIM:0'][0], IrresolvableBioEntity)

    def test_inputs_with_undefined_semantic_type_should_be_correctly_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'undefined': ['NCBIGene:1017']})
        self.assertIn('NCBIGene:1017', res)
        self.assertIsInstance(res['NCBIGene:1017'][0], ResolvableBioEntity)
        self.assertEqual(res['NCBIGene:1017'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0].label, 'CDK2')
        self.assertEqual(res['NCBIGene:1017'][0].semantic_type, 'Gene')

    def test_inputs_with_undefined_semantic_type_and_could_be_mapped_to_multiple_semantic_types_should_be_correctly_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'undefined': ['UMLS:C0008780']})
        self.assertIn('UMLS:C0008780', res)
        valid = [rec for rec in res['UMLS:C0008780'] if isinstance(rec, ResolvableBioEntity)]
        self.assertEqual(len(valid), 2)
        self.assertEqual(valid[0].semantic_type, 'PhenotypicFeature')
        self.assertEqual(valid[1].primary_id, 'MONDO:0016575')
        self.assertEqual(valid[1].label, 'primary ciliary dyskinesia')
        self.assertEqual(valid[1].semantic_type, 'Disease')

    def test_inputs_with_undefined_semantic_type_and_could_be_mapped_to_multiple_semantic_types_correctly_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'undefined': ['OMIM:116953']})
        self.assertIn('OMIM:116953', res)
        self.assertIsInstance(res['OMIM:116953'][0], ResolvableBioEntity)
        self.assertEqual(res['OMIM:116953'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['OMIM:116953'][0].label, 'CDK2')
        self.assertEqual(res['OMIM:116953'][0].semantic_type, 'Gene')

    def test_inputs_with_undefined_semantic_type_and_could_not_be_mapped_to_any_semantic_type_return_irresolvable(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'undefined': ['OMIM1:116953']})
        self.assertIn('OMIM1:116953', res)
        self.assertIsInstance(res['OMIM1:116953'][0], IrresolvableBioEntity)
        self.assertEqual(res['OMIM1:116953'][0].semantic_type, 'undefined')

    def test_irresolvable_inputs_should_not_overwrite_the_result_of_a_valid_input(self):
        resolver = DefaultResolver()
        res = resolver.resolve({"Gene": ["NCBIGene:1017"], "Disease": ["NCBIGene:1017"]})
        self.assertIn('NCBIGene:1017', res)
        self.assertEqual(len(res['NCBIGene:1017']), 2)
        self.assertIsInstance(res['NCBIGene:1017'][0], ResolvableBioEntity)
        self.assertEqual(res['NCBIGene:1017'][0].primary_id, 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0].label, 'CDK2')
        self.assertIsInstance(res['NCBIGene:1017'][1], IrresolvableBioEntity)

    # FIX ME
    def test_chemical_attributes_are_correctly_retrieved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'SmallMolecule': ['CHEMBL.COMPOUND:CHEMBL744']})
        self.assertIn('Benzothiazoles', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['drugbank_taxonomy_class'])
        self.assertIn('4', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['chembl_max_phase'])
        self.assertIn('Small molecule', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['chembl_molecule_type'])
        self.assertIn('Anticonvulsants', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['drugbank_drug_category'])
        self.assertIn('approved', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['drugbank_groups'])
        self.assertIn('Organic compounds', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['drugbank_kingdom'])
        self.assertIn('Organoheterocyclic compounds', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['drugbank_superclass'])
        self.assertIn('Drug-induced hepatitis', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['contraindications'])
        self.assertIn('Amyotrophic lateral sclerosis', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['indications'])
        self.assertIn('Anticonvulsants', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['mesh_pharmacology_class'])
        self.assertIn('Benzothiazole', res['CHEMBL.COMPOUND:CHEMBL744'][0].attributes['fda_epc_pharmacology_class'])

    def test_variant_attributes_are_correctly_retrieved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'SequenceVariant': ['DBSNP:rs796065306']})
        self.assertIn('NON_SYNONYMOUS', res['DBSNP:rs796065306'][0].attributes['cadd_consequence'])
        self.assertIn('SNV', res['DBSNP:rs796065306'][0].attributes['cadd_variant_type'])
        self.assertIn('snv', res['DBSNP:rs796065306'][0].attributes['dbsnp_variant_type'])
        self.assertIn('Pathogenic', res['DBSNP:rs796065306'][0].attributes['clinvar_clinical_significance'])
        self.assertIn('deleterious', res['DBSNP:rs796065306'][0].attributes['sift_category'])

    def test_gene_attributes_are_correctly_retrieved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Gene': ['NCBIGene:1017']})
        self.assertIn('Protein kinase domain', res['NCBIGene:1017'][0].attributes['interpro'])
        self.assertIn('protein-coding', res['NCBIGene:1017'][0].attributes['type_of_gene'])

    def test_pathway_attributes_are_correctly_retrieved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Pathway': ['WIKIPATHWAYS:WP151']})
        self.assertIn('68', res['WIKIPATHWAYS:WP151'][0].attributes['num_of_participants'])

    def test_snomedct_id_are_correctly_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Disease': ["SNOMEDCT:49455004"]})
        self.assertIsInstance(res["SNOMEDCT:49455004"][0], ResolvableBioEntity)

    def test_ncit_id_are_correctly_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'Disease': ["NCIT:C116936"]})
        self.assertIsInstance(res["NCIT:C116936"][0], ResolvableBioEntity)

    # FIX ME
    def test_chemical_ids_can_be_resolved_as_rhea_ids(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'SmallMolecule': ["PUBCHEM.COMPOUND:5460389"]})
        self.assertIsInstance(res['PUBCHEM.COMPOUND:5460389'][0], ResolvableBioEntity)
        self.assertIn('RHEA', res["PUBCHEM.COMPOUND:5460389"][0].db_ids)
        self.assertIn('RHEA:37975', res["PUBCHEM.COMPOUND:5460389"][0].db_ids['RHEA'])

    #@unittest.SkipTest
    def test_rhea_ids_can_be_correctly_resolved(self):
        resolver = DefaultResolver()
        res = resolver.resolve({'MolecularActivity': ['RHEA:37975']})
        self.assertIsInstance(res['RHEA:37975'][0], ResolvableBioEntity)
        self.assertEqual(res['RHEA:37975'][0].primary_id, 'GO:0010176')
