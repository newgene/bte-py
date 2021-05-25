import unittest
from biothings_explorer.biolink_model.object.entity_object import Entity


class TestEntityObjectClass(unittest.TestCase):
    def test_if_input_is_gene_should_add_additional_id_prefixes(self):
        entity = Entity('Gene', {'id_prefixes': ['NCBIGene']})
        self.assertIn('NCBIGene', entity.id_prefixes)
        self.assertIn('UMLS', entity.id_prefixes)
        self.assertIn('SYMBOL', entity.id_prefixes)
        self.assertIn('OMIM', entity.id_prefixes)

    def test_if_input_is_chemicalsubstance_should_add_additional_id_prefixes(self):
        entity = Entity('ChemicalSubstance', {'id_prefixes': ['CHEMBL.COMPOUND']})
        self.assertIn('CHEMBL.COMPOUND', entity.id_prefixes)
        self.assertIn('UMLS', entity.id_prefixes)

    def test_if_input_is_disease_just_return_the_provided_ones(self):
        entity = Entity('Disease', {'id_prefixes': ['KEGG']})
        self.assertEqual(len(entity.id_prefixes), 2)
        self.assertIn('KEGG', entity.id_prefixes)
        self.assertIn('GARD', entity.id_prefixes)

    def test_if_input_is_not_gene_or_chemicalsubstance_should_just_return_provided_ones(self):
        entity = Entity('PhenotypicFeature', {'id_prefixes': ['HP']})
        self.assertEqual(len(entity.id_prefixes), 1)
        self.assertIn('HP', entity.id_prefixes)
