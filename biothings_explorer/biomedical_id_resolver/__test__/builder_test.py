import unittest
from biothings_explorer.biomedical_id_resolver.query.builder.biothings_builder import BioThingsQueryBuilder
from biothings_explorer.biomedical_id_resolver.bioentity.valid_bioentity import ResolvableBioEntity
from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity
from ..config import APIMETA


class TestBioThingsQueryBuilderClass(unittest.TestCase):
    def test_biothings_api_response_are_correctly_passed(self):
        response = [
            {
                "query": "1017",
                "entrezgene": "1017",
                "symbol": "CDK2"
            },
            {
                "query": "1019",
                "entrezgene": "1019",
                "symbol": "CDK4"
            }
        ]

        builder = BioThingsQueryBuilder('Gene', ["NCBIGene:1017", "NCBIGene:1018"])
        res = builder.get_db_ids('NCBIGene', 'Gene', response)
        self.assertIn('NCBIGene:1017', res)
        self.assertIn('NCBIGene:1019', res)
        self.assertIsInstance(res['NCBIGene:1017'], ResolvableBioEntity)
        entity = res['NCBIGene:1017']
        self.assertEqual(entity.primary_id, 'NCBIGene:1017')

    def test_failed_record_should_be_classified_as_unresolved(self):
        response = [
            {
                "query": "1017",
                "entrezgene": "1017",
                "symbol": "CDK2"
            },
            {
                "query": "1019",
                "notfound": True,
                "entrezgene": "1019",
                "symbol": "CDK4"
            }
        ]

        builder = BioThingsQueryBuilder('Gene', ["NCBIGene:1017", "NCBIGene:1018"])
        res = builder.get_db_ids('NCBIGene', 'Gene', response)
        self.assertIn('NCBIGene:1017', res)
        self.assertIn('NCBIGene:1019', res)
        self.assertIsInstance(res['NCBIGene:1019'], IrresolvableBioEntity)

    def test_build_one_query_function(self):
        builder = BioThingsQueryBuilder('Gene', ["NCBIGene:1017", "NCBIGene:1018"])
        res = builder.build_one_query(APIMETA['Gene'], "NCBIGene", ["1017", "1018"])
        self.assertIn('NCBIGene:1017', res)

    def test_inputs_with_less_than_1000_ids_should_return_one_promise(self):
        builder = BioThingsQueryBuilder('Gene', ["NCBIGene:1017", "NCBIGene:1018"])
        res = builder.build_queries(APIMETA['Gene'], "NCBIGene", ["1017", "1018"])
        self.assertEqual(len(res), 1)
        #Concept of promise missing in python, can't really test it

    def test_inputs_with_more_than_1000_ids_should_return_more_than_one_promise(self):
        fake_inputs = ['NCBIGene:' + str(item) for item in range(1990)]
        builder = BioThingsQueryBuilder('Gene', fake_inputs)
        res = builder.build_queries(APIMETA['Gene'], "NCBIGene", fake_inputs)
        self.assertEqual(len(res), 2)

    def test_inputs_with_a_mix_of_ids_with_different_prefixes(self):
        builder = BioThingsQueryBuilder('Gene', ["NCBIGene:1017", "OMIM:1018"])
        res = builder.build()
        self.assertEqual(len(res), 2)

    def test_inputs_with_more_than_1000_ids_should_return_more_than_one_promise(self):
        fake_ncbi_gene_inputs = ['NCBIGene:' + str(item) for item in range(1990)]
        fake_omim_gene_inputs = ['OMIM:' + str(item) for item in range(2300)]
        builder = BioThingsQueryBuilder('Gene', [*fake_ncbi_gene_inputs, *fake_omim_gene_inputs])
        res = builder.build()
        self.assertEqual(len(res), 5)
