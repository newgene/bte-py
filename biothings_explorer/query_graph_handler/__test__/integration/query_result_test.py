import unittest
from biothings_explorer.query_graph_handler.query_node import QNode
from biothings_explorer.query_graph_handler.query_edge import QEdge
from biothings_explorer.query_graph_handler.query_results import QueryResult


class TestQueryResults(unittest.TestCase):
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
                "curies": ['CHEMBL.COMPOUND:CHEMBL744', 'PUBCHEM:1234', "name:RILUZOLE"]
            }]
        },
    }

    def test_create_node_bindings_test_when_input_with_string_should_output_a_has_of_40_characters(self):
        query_result = QueryResult()
        res = query_result._create_node_bindings(self.record)
        self.assertIn('n1', res)
        self.assertIn('n3', res)
        self.assertEqual('NCBIGene:1017', res['n1'][0]['id'])
        self.assertEqual('CHEMBL.COMPOUND:CHEMBL744', res['n3'][0]['id'])

    def test_create_edge_bindings_when_input_with_string_should_output_a_hash_of_40_characters(self):
        query_result = QueryResult()
        res = query_result._create_edge_bindings(self.record)
        self.assertIn('e01', res)
        self.assertEqual(len(res['e01']), 1)

    def test_update_when_input_with_string_should_output_a_hash_of_40_characters(self):
        query_result = QueryResult()
        query_result.update([self.record])
        self.assertEqual(len(query_result.results), 1)
        self.assertIn('n1', query_result.results[0]['node_bindings'])
        self.assertIn('e01', query_result.results[0]['edge_bindings'])