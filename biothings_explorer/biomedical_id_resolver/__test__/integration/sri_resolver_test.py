import unittest
from biothings_explorer.biomedical_id_resolver.resolver import resolve_sri


class TestSRIResolver(unittest.TestCase):
    def test_old_format(self):
        _input = {
            "Gene": ["NCBIGene:1017", "NCBIGene:1018", "HGNC:1177"],
            "SmallMolecule": ["CHEBI:15377"],
            "Disease": ["MONDO:0004976"],
            "Cell": ["CL:0002372"]
        }

        res = resolve_sri(_input)
        self.assertEqual(res['NCBIGene:1017'][0]['primaryID'], 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0]['label'], 'CDK2')
        self.assertEqual(res["NCBIGene:1017"][0]['semanticType'], 'Gene')
        self.assertIsInstance(res["NCBIGene:1017"][0]['semanticTypes'], list)
        self.assertIsInstance(res["NCBIGene:1017"][0]['dbIDs'], dict)

    def test_array_of_curries(self):
        _input = ["NCBIGene:1017", "MONDO:0004976"]
        res = resolve_sri(_input)
        self.assertEqual(res['NCBIGene:1017'][0]['primaryID'], 'NCBIGene:1017')
        self.assertEqual(res['NCBIGene:1017'][0]['label'], 'CDK2')
        self.assertEqual(res["NCBIGene:1017"][0]['semanticType'], 'Gene')
        self.assertIsInstance(res["NCBIGene:1017"][0]['semanticTypes'], list)
        self.assertIsInstance(res["NCBIGene:1017"][0]['dbIDs'], dict)

    def test_unresolvable_curie(self):
        _input = ["NCBIGene:ABCD"]
        res = resolve_sri(_input)
        self.assertEqual(res['NCBIGene:ABCD'][0]['primaryID'], 'NCBIGene:ABCD')
        self.assertEqual(res['NCBIGene:ABCD'][0]['label'], 'NCBIGene:ABCD')

