import unittest
from biothings_explorer.biomedical_id_resolver.index import METADATA, Resolver
from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity


class TestResolverModule(unittest.TestCase):
    def test_resolver_class_should_be_set_correctly_if_given_type_biolink(self):
        resolver = Resolver('biolink')
        res = resolver.resolve({'NamedThing': ['NCBIGene:1017']})
        self.assertIn('NamedThing', res['NCBIGene:1017'][0].semantic_types)
        self.assertEqual(res['NCBIGene:1017'][0].semantic_type, 'Gene')

    def test_resolver_class_should_be_set_correctly_if_given_undefined(self):
        resolver = Resolver()
        res = resolver.resolve({'NamedThing': ['NCBIGene:1017']})
        self.assertIn('NamedThing', res['NCBIGene:1017'][0].semantic_types)
        self.assertIsInstance(res['NCBIGene:1017'][0], IrresolvableBioEntity)


class TestApiMetadataIsCorrectlyExported(unittest.TestCase):
    def test_gene_should_be_part_of_metadata(self):
        self.assertIn('Gene', METADATA)