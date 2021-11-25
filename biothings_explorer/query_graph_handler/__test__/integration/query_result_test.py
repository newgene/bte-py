import unittest
from biothings_explorer.query_graph_handler.query_node import QNode
from biothings_explorer.query_graph_handler.query_edge import QEdge
from biothings_explorer.query_graph_handler.query_results import QueryResult


class TestQueryResults(unittest.TestCase):
    def test_single_record(self):
        gene_node1 = QNode('n1', {'categories': ['Gene'], 'ids': ['NCBIGene:632']})
        chemical_node1 = QNode('n2', { 'categories': ['ChemicalSubstance']})
        edge1 = QEdge('e01', {'subject': gene_node1, 'object': chemical_node1})
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge1,
                'predicate': 'biolink:physically_interacts_with',
                'source': 'DGIdb',
                'api_name': 'BioThings DGIDB API',
            },
            'publications': ['PMID:8366144', 'PMID:8381250'],
            'relation': 'antagonist',
            'source': 'DrugBank',
            'score': '0.9',
            '$input': {
                'original': 'SYMBOL:BGLAP',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:632',
                        'label': 'BGLAP',
                        'dbIDs': {
                            'SYMBOL': 'BGLAP',
                            'NCBIGene': '632',
                        },
                        'curies': ['SYMBOL:BGLAP', 'NCBIGene:632'],
                    },
                ],
            },
            '$output': {
                'original': 'CHEMBL.COMPOUND:CHEMBL1200983',
                'obj': [
                    {
                        'primaryID': 'CHEMBL.COMPOUND:CHEMBL1200983',
                        'label': 'GALLIUM NITRATE',
                        'dbIDs': {
                            'CHEMBL.COMPOUND': 'CHEMBL1200983',
                            'PUBCHEM.COMPOUND': '5282394',
                            'name': 'GALLIUM NITRATE',
                        },
                        'curies': ['CHEMBL.COMPOUND:CHEMBL1200983', 'PUBCHEM.COMPOUND:5282394', 'name:GALLIUM NITRATE'],
                    },
                ],
            },
        }
        query_result = QueryResult()
        query_result.update({
            'e01': {
                'connected_to': [],
                'records': [record]
            }
        })
        self.assertEqual(len(query_result.get_results()), 1)
        self.assertIn('n1', query_result.get_results()[0]['node_bindings'])
        self.assertIn('n2', query_result.get_results()[0]['node_bindings'])
        self.assertIn('e01', query_result.get_results()[0]['node_bindings'])
        self.assertIn('score', query_result.get_results()[0])
