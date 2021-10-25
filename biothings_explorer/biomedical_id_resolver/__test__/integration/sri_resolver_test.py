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

    def test_unresolvable_curie(self):
        _input = {
            "Gene": ["NCBIGene:ABCD"],
        }
        res = resolve_sri(_input)
        self.assertEqual(res['NCBIGene:ABCD'][0]['semanticType'], 'Gene')
        self.assertEqual(res['NCBIGene:ABCD'][0]['primaryID'], 'NCBIGene:ABCD')
        self.assertEqual(res['NCBIGene:ABCD'][0]['label'], 'NCBIGene:ABCD')
        self.assertIsInstance(res['NCBIGene:ABCD'][0]['dbIDs']['name'], list)
        self.assertIsInstance(res['NCBIGene:ABCD'][0]['dbIDs']['NCBIGene'], list)

    def test_using_sri_to_get_semantic_types(self):
        _input = {
            'unknown': ["NCBIGene:1017"]
        }
        res = resolve_sri(_input)
        self.assertEqual(len(res['NCBIGene:1017']), 1)
        self.assertEqual(res['NCBIGene:1017'][0]['semanticType'], 'Gene')

    def test_handling_semantic_type_conflicts(self):
        _input = {
            "SmallMolecule": ["PUBCHEM.COMPOUND:23680530"]
        }
        res = resolve_sri(_input)
        self.assertEqual(len(res['PUBCHEM.COMPOUND:23680530']), 2)
        self.assertEqual(res['PUBCHEM.COMPOUND:23680530'][0]['semanticType'], 'MolecularMixture')
        self.assertEqual(res['PUBCHEM.COMPOUND:23680530'][1]['semanticType'], 'SmallMolecule')

    def test_sri_semantic_type_resolver(self):
        _input = {
            'unknown': ['NCBIGene:3778']
        }
        res = resolve_sri(_input)
        self.assertIsInstance(res['NCBIGene:3778'], list)
        self.assertEqual(res['NCBIGene:3778'][0]['semanticType'], 'Gene')

    def test_same_id_different_semantic_types(self):
        _input = {
            "Gene": ["NCBIGene:1017"],
            "Disease": ["NCBIGene:1017"]
        }

        res = resolve_sri(_input)
        self.assertGreater(len(res['NCBIGene:1017']), 1)
