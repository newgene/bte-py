import unittest
from biothings_explorer.biomedical_id_resolver.bioentity.valid_bioentity import ResolvableBioEntity
from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity

CDK2_DB_IDs = {
    "NCBIGene": ["1017"],
    "HGNC": ["1771"],
    "SYMBOL": ["CDK2"],
    "name": ["cyclin dependent kinase 2"],
}

RILUZOLE_DB_IDS = {
    "CHEMBL.COMPOUND": ["CHEMBL744"],
    "name": ["Riluzole", "RILUZOLE"],
    "PUBCHEM.COMPOUND": ["5070"],
}

DB_ID_WITH_NO_PRIMARY = {
    "kk": ["kkk"]
}

DISEASE_DB_IDS = {
    "MONDO": ["MONDO:12345"]
}

CHEMBL7512_DB_IDS = { "CHEMBL.COMPOUND": ["CHEMBL7512"], "PUBCHEM.COMPOUND": ["53428"] }


class TestResolvableBioEntityClass(unittest.TestCase):
    def test_return_semantic_type_when_called_semantic_type_property(self):
        entity = ResolvableBioEntity('Gene', CDK2_DB_IDs, {})
        res = entity.semantic_type
        self.assertEqual(res, 'Gene')

    def test_db_ids_with_prefixes_defined_in_metadata_should_return_the_primary_id(self):
        entity = ResolvableBioEntity('Gene', CDK2_DB_IDs, {})
        primary_id = entity.primary_id
        self.assertEqual(primary_id, 'NCBIGene:1017')

    def test_db_ids_always_prefixed_should_return_itself(self):
        entity = ResolvableBioEntity('Disease', DISEASE_DB_IDS, {})
        primary_id = entity.primary_id
        self.assertEqual(primary_id, 'MONDO:12345')

    def test_db_ids_without_prefixes_defined_in_metadata_should_return_undefined(self):
        entity = ResolvableBioEntity('Gene', DB_ID_WITH_NO_PRIMARY, {})
        primary_id = entity.primary_id
        self.assertIsNone(primary_id)

    def test_if_symbol_provided_in_db_ids_should_return_symbol(self):
        entity = ResolvableBioEntity('Gene', CDK2_DB_IDs, {})
        label = entity.label
        self.assertEqual('CDK2', label)

    def test_if_symbol_not_provided_in_db_ids_and_name_is_provided_should_return_name(self):
        entity = ResolvableBioEntity('SmallMolecule', RILUZOLE_DB_IDS, {})
        label = entity.label
        self.assertEqual(label, 'Riluzole')

    def test_if_both_symbol_and_name_are_not_provided_in_ids_should_return_primary_id(self):
        entity = ResolvableBioEntity('SmallMolecule', CHEMBL7512_DB_IDS, {})
        label = entity.label
        self.assertEqual(label, 'PUBCHEM.COMPOUND:53428')

    def test_get_curies(self):
        entity = ResolvableBioEntity('SmallMolecule', CHEMBL7512_DB_IDS, {})
        curies = entity.curies
        self.assertIn('CHEMBL.COMPOUND:CHEMBL7512', curies)
        self.assertEqual(len(curies), 2)

    def test_get_db_ids(self):
        entity = ResolvableBioEntity('SmallMolecule', CHEMBL7512_DB_IDS, {})
        db_ids = entity.db_ids
        self.assertEqual(db_ids, CHEMBL7512_DB_IDS)


class TestIrresolvableBioEntityClass(unittest.TestCase):
    def test_return_semantic_type_when_called_semantic_type_property(self):
        entity = IrresolvableBioEntity('Gene', 'KK:123')
        res = entity.semantic_type
        self.assertEqual('Gene', res)

    def test_should_return_the_input_curie(self):
        entity = IrresolvableBioEntity('Gene', 'KK:123')
        primary_id = entity.primary_id
        self.assertEqual(primary_id, 'KK:123')

    def test_label_function_should_return_the_input_curie(self):
        entity = IrresolvableBioEntity('Gene', 'KK:123')
        label = entity.label
        self.assertEqual(label, 'KK:123')

    def test_get_curies_function(self):
        entity = IrresolvableBioEntity('SmallMolecule', 'KK:123')
        curies = entity.curies
        self.assertEqual(curies, ['KK:123'])

    def test_get_db_ids(self):
        entity = IrresolvableBioEntity('SmallMolecule', 'KK:123')
        db_ids = entity.db_ids
        self.assertEqual(db_ids, {'KK': ['KK:123']})

    def test_get_attributes_function(self):
        entity = IrresolvableBioEntity('SmallMolecule', 'KK:123')
        attributes = entity.attributes
        self.assertEqual(attributes, {})

