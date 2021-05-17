import unittest
from biothings_explorer.smartapi_kg.filter import ft

ops = [
        {
            'association': {
                "input_type": "Gene",
                "input_id": "NCBIGENE",
                "output_type": "Disease",
                "output_id": "MONDO",
                "predicate": "PRED1",
                "source": "SOURCE1"
            }
        },
        {
            "association": {
                "input_type": "SequenceVariant",
                "input_id": "NCBIGENE",
                "output_type": "ChemicalSubstance",
                "output_id": "CHEBI",
                "predicate": "PRED2",
                "source": "SOURCE2",
                "api_name": "API1"
            }
        },
        {
            "association": {
                "input_type": "Gene",
                "input_id": "NCBIGENE",
                "output_type": "ChemicalSubstance",
                "output_id": "CHEBI",
                "predicate": "PRED3",
                "source": "SOURCE3"
            }
        },
        {
            "association": {
                "input_type": "Gene",
                "input_id": "NCBIGENE",
                "output_type": "Disease",
                "output_id": "MONDO",
                "predicate": "PRED2",
                "source": "SOURCE3",
                "api_name": "API1"
            }
        },
    ]


class TestFilter(unittest.TestCase):
    def test_return_only_ops_with_gene_when_specifying_as_gene_in_string(self):
        res = ft(ops, {'input_type': 'Gene'})
        self.assertEqual(len([op for op in ops if op['association']['input_type']=='Gene']), len(res))
        self.assertEqual(res[0]['association']['source'], 'SOURCE1')

    def test_return_only_ops_with_gene_when_specifying_as_gene_in_array(self):
        res = ft(ops, {'input_type': ["Gene"]})
        self.assertEqual(len([op for op in ops if op['association']['input_type']=='Gene']), len(res))
        self.assertEqual(res[0]['association']['source'], 'SOURCE1')

    def test_return_only_ops_with_output_gene_when_specifying_output_as_chemicalsubstance_in_string(self):
        res = ft(ops, {'output_type': 'ChemicalSubstance'})
        self.assertEqual(len([op for op in ops if op['association']['output_type']=='ChemicalSubstance']), len(res))
        self.assertEqual(res[0]['association']['source'], 'SOURCE2')

    def test_return_only_ops_with_predicate_PRED2_when_specifying_preficate_as_PRED2_in_string(self):
        res = ft(ops, {'predicate': 'PRED2'})
        self.assertEqual(len([op for op in ops if op['association']['predicate']=='PRED2']), len(res))
        self.assertEqual(res[0]['association']['source'], 'SOURCE2')

    def test_return_only_ops_with_gene_and_output_disease_when_specifying_input_as_gene_and_output_as_disease(self):
        res = ft(ops, {'input_type': 'Gene', 'output_type': 'Disease'})
        self.assertEqual(len([op for op in ops if op['association']['input_type']=='Gene' and
                              op['association']['output_type']=='Disease']), len(res))
        self.assertEqual(res[0]['association']['source'], 'SOURCE1')

    def test_return_only_ops_with_input_type_gene_and_output_disease(self):
        res = ft(ops, {'input_type': 'Gene', 'output_type': ['Disease', 'ChemicalSubstance']})
        self.assertEqual(len([op for op in ops if op['association']['input_type'] == 'Gene' and
                              op['association']['output_type'] in ['Disease', 'ChemicalSubstance']]), len(res))
        self.assertEqual(res[0]['association']['source'], 'SOURCE1')

    def test_return_empty_array_when_cant_find_match(self):
        res = ft(ops, {'input_type': 'Gene1', 'output_type': ['Disease', 'ChemicalSubstance']})
        self.assertEqual(len(res), 0)


if __name__ == '__main__':
    unittest.main()
