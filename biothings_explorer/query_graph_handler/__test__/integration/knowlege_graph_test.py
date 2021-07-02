import unittest
from biothings_explorer.query_graph_handler.query_node import QNode
from biothings_explorer.query_graph_handler.query_edge import QEdge
from biothings_explorer.query_graph_handler.knowledge_graph import KnowledgeGraph


class TestingKnowledgeGraph(unittest.TestCase):
    gene_node1 = QNode('n1', {'categories': 'Gene', 'ids': 'NCBIGene:1017'})
    chemical_node1 = QNode('n3', {'categories': 'ChemicalSubstance'})
    edge1 = QEdge('e01', {'subject': gene_node1, 'object': chemical_node1})
    record = {
        "$edge_metadata": {
            "trapi_qEdge_obj": edge1,
            "source": "DGIdb",
            "api_name": "BioThings DGIDB API"
        },
        "publications": ['PMID:123', 'PMID:1234'],
        "interactionType": "inhibitor",
        "$input": {
            "original": "SYMBOL:CDK2",
            "obj": [{
                "primaryID": 'NCBIGene:1017',
                "label": "CDK2",
                "dbIDs": {
                    "SYMBOL": "CDK2",
                    "NCBIGene": "1017"
                },
                "semanticType": "Gene",
                "curies": ['SYMBOL:CDK2', 'NCBIGene:1017']
            }]
        },
        "$output": {
            "original": "CHEMBL.COMPOUND:CHEMBL744",
            "obj": [{
                "primaryID": 'CHEMBL.COMPOUND:CHEMBL744',
                "label": "RILUZOLE",
                "dbIDs": {
                    "CHEMBL.COMPOUND": "CHEMBL744",
                    "PUBCHEM": "1234",
                    "name": "RILUZOLE"
                },
                "semanticType": "ChemicalSubstance",
                "curies": ['CHEMBL.COMPOUND:CHEMBL744', 'PUBCHEM:1234', "name:RILUZOLE"]
            }]
        },
    }

    def test_create_input_node_when_input_with_string_should_output_a_hash_of_40_characters(self):
        kg = KnowledgeGraph()
        res = kg._create_input_node(self.record)
        self.assertIn('categories', res)
        self.assertEqual(res['categories'], 'biolink:Gene')
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'CDK2')
        self.assertIn('type', res['attributes'][0])
        self.assertEqual(res['attributes'][0]['type'], 'biolink:id')
        self.assertIn('value', res['attributes'][0])
        self.assertEqual(res['attributes'][0]['value'], ["SYMBOL:CDK2", "NCBIGene:1017"])

    def test_create_output_node_test_when_input_with_string_should_output_a_hash_of_40_characters(self):
        kg = KnowledgeGraph()
        res = kg._create_output_node(self.record)
        self.assertIn('categories', res)
        self.assertEqual(res['categories'], 'biolink:ChemicalSubstance')
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'RILUZOLE')
        self.assertIn('type', res['attributes'][0])
        self.assertEqual(res['attributes'][0]['type'], 'biolink:id')
        self.assertIn('value', res['attributes'][0])
        self.assertEqual(res['attributes'][0]['value'], ['CHEMBL.COMPOUND:CHEMBL744', 'PUBCHEM:1234', "name:RILUZOLE"])

    def test_create_attributes_edge_attribute_provided_by_and_api_are_correctly_found(self):
        kg = KnowledgeGraph()
        res = kg._create_attributes(self.record)
        self.assertGreaterEqual(len(res), 2)
        self.assertIn('name', res[0])
        self.assertEqual(res[0]['name'], 'provided_by')
        self.assertIn('type', res[0])
        self.assertEqual(res[0]['type'], 'biolink:provided_by')
        self.assertIn('value', res[0])
        self.assertEqual(res[0]['value'], 'DGIdb')
        self.assertIn('name', res[1])
        self.assertEqual(res[1]['name'], 'api')
        self.assertIn('type', res[1])
        self.assertEqual(res[1]['type'], 'bts:api')
        self.assertIn('value', res[1])
        self.assertEqual(res[1]['value'], 'BioThings DGIDB API')

    def test_create_attributes_edge_attribute_other_than_provided_by_and_api_are_correctly_found(self):
        kg = KnowledgeGraph()
        res = kg._create_attributes(self.record)
        self.assertGreaterEqual(len(res), 2)
        self.assertIn('name', res[2])
        self.assertEqual(res[2]['name'], 'publications')
        self.assertIn('type', res[2])
        self.assertEqual(res[2]['type'], 'biolink:publications')
        self.assertIn('value', res[2])
        self.assertEqual(res[2]['value'], ['PMID:123', 'PMID:1234'])
        self.assertIn('name', res[3])
        self.assertEqual(res[3]['name'], 'interactionType')
        self.assertIn('type', res[3])
        self.assertEqual(res[3]['type'], 'bts:interactionType')
        self.assertIn('value', res[3])
        self.assertEqual(res[3]['value'], 'inhibitor')

    def test_create_edge_edge_attribute_provided_by_and_api_are_correctly_found(self):
        kg = KnowledgeGraph()
        res = kg._create_attributes(self.record)
        self.assertGreaterEqual(len(res), 2)
        self.assertIn('name', res[0])
        self.assertEqual(res[0]['name'], 'provided_by')
        self.assertIn('type', res[0])
        self.assertEqual(res[0]['type'], 'biolink:provided_by')
        self.assertIn('value', res[0])
        self.assertEqual(res[0]['value'], 'DGIdb')
        self.assertIn('name', res[1])
        self.assertEqual(res[1]['name'], 'api')
        self.assertIn('type', res[1])
        self.assertEqual(res[1]['type'], 'bts:api')
        self.assertIn('value', res[1])
        self.assertEqual(res[1]['value'], 'BioThings DGIDB API')

    def test_create_edge_edge_attribute_other_than_provided_by_and_api_are_correctly_found(self):
        kg = KnowledgeGraph()
        res = kg._create_attributes(self.record)
        self.assertGreaterEqual(len(res), 2)
        self.assertIn('name', res[2])
        self.assertEqual(res[2]['name'], 'publications')
        self.assertIn('type', res[2])
        self.assertEqual(res[2]['type'], 'biolink:publications')
        self.assertIn('value', res[2])
        self.assertEqual(res[2]['value'], ['PMID:123', 'PMID:1234'])
        self.assertIn('name', res[3])
        self.assertEqual(res[3]['name'], 'interactionType')
        self.assertIn('type', res[3])
        self.assertEqual(res[3]['type'], 'bts:interactionType')
        self.assertIn('value', res[3])
        self.assertEqual(res[3]['value'], 'inhibitor')