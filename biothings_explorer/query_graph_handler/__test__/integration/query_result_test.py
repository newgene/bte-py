import unittest
from biothings_explorer.query_graph_handler.query_node import QNode
from biothings_explorer.query_graph_handler.query_edge import QEdge
from biothings_explorer.query_graph_handler.query_results import QueryResult


class TestQueryResults(unittest.TestCase):
    gene_node1 = QNode('n1', {'categories': 'Gene', 'ids': 'NCBIGene:NCBIGene'})
    chemical_node1 = QNode('n2', {'categories': 'ChemicalSubstance'})
    edge1 = QEdge('e01', {'subject': gene_node1, 'object': chemical_node1})
    record = {
        "$edge_metadata": {
            "trapi_qEdge_obj": edge1,
            "predicate": "biolink:physically_interacts_with",
            "source": "DGIdb",
            "api_name": "BioThings DGIDB API"
        },
        "publications": [
            "PMID:8366144",
            "PMID:8381250"
        ],
        "relation": "antagonist",
        "source": "DrugBank",
        "score": "0.9",
        "$input": {
            "original": "SYMBOL:BGLAP",
            "obj": [
                {
                    "primaryID": "NCBIGene:632",
                    "label": "BGLAP",
                    "dbIDs": {
                        "SYMBOL": "BGLAP",
                        "NCBIGene": "632"
                    },
                    "curies": [
                        "SYMBOL:BGLAP",
                        "NCBIGene:632"
                    ]
                }
            ]
        },
        "$output": {
            "original": "CHEMBL.COMPOUND:CHEMBL1200983",
            "obj": [
                {
                    "primaryID": "CHEMBL.COMPOUND:CHEMBL1200983",
                    "label": "GALLIUM NITRATE",
                    "dbIDs": {
                        "CHEMBL.COMPOUND": "CHEMBL1200983",
                        "PUBCHEM.COMPOUND": "5282394",
                        "name": "GALLIUM NITRATE"
                    },
                    "curies": [
                        "CHEMBL.COMPOUND:CHEMBL1200983",
                        "PUBCHEM.COMPOUND:5282394",
                        "name:GALLIUM NITRATE"
                    ]
                }
            ]
        }
    }

    def test_create_node_bindings_when_input_with_string_should_output_a_has_of_40_characters(self):
        query_result = QueryResult()
        res = query_result._create_node_bindings(self.record)
        self.assertIn('n1', res)
        self.assertIn('n2', res)
        self.assertEqual('NCBIGene:632', res['n1'][0]['id'])
        self.assertEqual('CHEMBL.COMPOUND:CHEMBL1200983', res['n2'][0]['id'])

    def test_create_edge_bindings_when_input_with_string_should_output_a_hash_of_40_characters(self):
        query_result = QueryResult()
        res = query_result._create_edge_bindings(self.record)
        self.assertIn('e01', res)
        self.assertEqual(len(res['e01']), 1)

    def test_update_when_input_with_string_should_output_a_hash_of_40_characters(self):
        query_result = QueryResult()
        query_result.update([self.record])
        self.assertEqual(len(query_result.get_results()), 1)
        self.assertIn('n1', query_result.get_results()[0]['node_bindings'])
        self.assertIn('e01', query_result.get_results()[0]['edge_bindings'])


class TestTwoRecords(unittest.TestCase):
    gene_node_start = QNode('n1', {'categories': 'Gene', 'ids': 'NCBIGene:3778'})
    disease_node = QNode('n2', {'categories': 'Disease'})
    gene_node_end = QNode('n3', {'categories': 'Gene'})
    edge1 = QEdge('e01', {'subject': gene_node_start, 'object': disease_node})
    edge2 = QEdge('e02', {'subject': disease_node, 'object': gene_node_end})

    record1 = {
        "$edge_metadata": {
            "trapi_qEdge_obj": edge1,
            "predicate": "biolink:gene_associated_with_condition",
            "api_name": "Automat Pharos"
        },
        "publications": [
            "PMID:123",
            "PMID:1234"
        ],
        "$input": {
            "original": "SYMBOL:KCNMA1",
            "obj": [
                {
                    "primaryID": "NCBIGene:3778",
                    "label": "KCNMA1",
                    "dbIDs": {
                        "SYMBOL": "KCNMA1",
                        "NCBIGene": "3778"
                    },
                    "curies": [
                        "SYMBOL:KCNMA1",
                        "NCBIGene:3778"
                    ]
                }
            ]
        },
        "$output": {
            "original": "MONDO:0011122",
            "obj": [
                {
                    "primaryID": "MONDO:0011122",
                    "label": "obesity disorder",
                    "dbIDs": {
                        "MONDO": "0011122",
                        "MESH": "D009765",
                        "name": "obesity disorder"
                    },
                    "curies": [
                        "MONDO:0011122",
                        "MESH:D009765",
                        "name:obesity disorder"
                    ]
                }
            ]
        }
    }
    record2 = {
        "$edge_metadata": {
            "trapi_qEdge_obj": edge2,
            "predicate": "biolink:condition_associated_with_gene",
            "api_name": "Automat Hetio"
        },
        "publications": [
            "PMID:345",
            "PMID:456"
        ],
        "$input": {
            "original": "MONDO:0011122",
            "obj": [
                {
                    "primaryID": "MONDO:0011122",
                    "label": "obesity disorder",
                    "dbIDs": {
                        "MONDO": "0011122",
                        "MESH": "D009765",
                        "name": "obesity disorder"
                    },
                    "curies": [
                        "MONDO:0011122",
                        "MESH:D009765",
                        "name:obesity disorder"
                    ]
                }
            ]
        },
        "$output": {
            "original": "SYMBOL:TULP3",
            "obj": [
                {
                    "primaryID": "NCBIGene:7289",
                    "label": "TULP3",
                    "dbIDs": {
                        "SYMBOL": "TULP3",
                        "NCBIGene": "7289"
                    },
                    "curies": [
                        "SYMBOL:TULP3",
                        "NCBIGene:7289"
                    ]
                }
            ]
        }
    }

    def test_update_function_should_get_n1_n2_n3_and_e01_e02(self):
        query_result = QueryResult()
        query_result.update([self.record1])
        query_result.update([self.record2])
        results = query_result.get_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]['node_bindings']), 3)
        self.assertIn('n1', results[0]['node_bindings'])
        self.assertIn('n2', results[0]['node_bindings'])
        self.assertIn('n3', results[0]['node_bindings'])
        self.assertEqual(len(results[0]['edge_bindings']), 2)
        self.assertIn('e01', results[0]['edge_bindings'])
        self.assertIn('e02', results[0]['edge_bindings'])


class TestThreeRecords(unittest.TestCase):
    gene_node_start = QNode('n1', {'categories': 'Gene', 'ids': 'NCBIGene:3778'})
    disease_node = QNode('n2', {'categories': 'Disease'})
    gene_node_end1 = QNode('n3', {'categories': 'Gene'})
    gene_node_end2 = QNode('n4', {'categories': 'Gene'})
    edge1 = QEdge('e01', {'subject': gene_node_start, 'object': disease_node})
    edge2 = QEdge('e02', {'subject': disease_node, 'object': gene_node_end1})
    edge3 = QEdge('e03', {'subject': disease_node, 'object': gene_node_end2})

    record1 = {
        "$edge_metadata": {
            "trapi_qEdge_obj": edge1,
            "predicate": "biolink:gene_associated_with_condition",
            "api_name": "Automat Pharos"
        },
        "publications": [
            "PMID:123",
            "PMID:1234"
        ],
        "$input": {
            "original": "SYMBOL:KCNMA1",
            "obj": [
                {
                    "primaryID": "NCBIGene:3778",
                    "label": "KCNMA1",
                    "dbIDs": {
                        "SYMBOL": "KCNMA1",
                        "NCBIGene": "3778"
                    },
                    "curies": [
                        "SYMBOL:KCNMA1",
                        "NCBIGene:3778"
                    ]
                }
            ]
        },
        "$output": {
            "original": "MONDO:0011122",
            "obj": [
                {
                    "primaryID": "MONDO:0011122",
                    "label": "obesity disorder",
                    "dbIDs": {
                        "MONDO": "0011122",
                        "MESH": "D009765",
                        "name": "obesity disorder"
                    },
                    "curies": [
                        "MONDO:0011122",
                        "MESH:D009765",
                        "name:obesity disorder"
                    ]
                }
            ]
        }
    }

    record2 = {
        "$edge_metadata": {
            "trapi_qEdge_obj": edge2,
            "predicate": "biolink:condition_associated_with_gene",
            "api_name": "Automat Hetio"
        },
        "publications": [
            "PMID:345",
            "PMID:456"
        ],
        "$input": {
            "original": "MONDO:0011122",
            "obj": [
                {
                    "primaryID": "MONDO:0011122",
                    "label": "obesity disorder",
                    "dbIDs": {
                        "MONDO": "0011122",
                        "MESH": "D009765",
                        "name": "obesity disorder"
                    },
                    "curies": [
                        "MONDO:0011122",
                        "MESH:D009765",
                        "name:obesity disorder"
                    ]
                }
            ]
        },
        "$output": {
            "original": "SYMBOL:TULP3",
            "obj": [
                {
                    "primaryID": "NCBIGene:7289",
                    "label": "TULP3",
                    "dbIDs": {
                        "SYMBOL": "TULP3",
                        "NCBIGene": "7289"
                    },
                    "curies": [
                        "SYMBOL:TULP3",
                        "NCBIGene:7289"
                    ]
                }
            ]
        }
    }

    record3 = {
        "$edge_metadata": {
            "trapi_qEdge_obj": edge3,
            "predicate": "biolink:condition_associated_with_gene",
            "api_name": "Automat Hetio"
        },
        "publications": [
            "PMID:987",
            "PMID:876"
        ],
        "$input": {
            "original": "MONDO:0011122",
            "obj": [
                {
                    "primaryID": "MONDO:0011122",
                    "label": "obesity disorder",
                    "dbIDs": {
                        "MONDO": "0011122",
                        "MESH": "D009765",
                        "name": "obesity disorder"
                    },
                    "curies": [
                        "MONDO:0011122",
                        "MESH:D009765",
                        "name:obesity disorder"
                    ]
                }
            ]
        },
        "$output": {
            "original": "SYMBOL:TECR",
            "obj": [
                {
                    "primaryID": "NCBIGene:9524",
                    "label": "TECR",
                    "dbIDs": {
                        "SYMBOL": "TECR",
                        "NCBIGene": "9524"
                    },
                    "curies": [
                        "SYMBOL:TECR",
                        "NCBIGene:9524"
                    ]
                }
            ]
        }
    }

    def test_update_function_should_get_a_single_hop_followed_by_a_forked_second_hop(self):
        query_result = QueryResult()
        query_result.update([self.record1])
        query_result.update([self.record2, self.record3])

        results = query_result.get_results()
        self.assertEqual(len(results), 2)
        self.assertEqual(len(results[0]['node_bindings']), 3)
        self.assertIn('n1', results[0]['node_bindings'])
        self.assertIn('n2', results[0]['node_bindings'])
        self.assertIn('n3', results[0]['node_bindings'])

        self.assertEqual(len(results[0]['edge_bindings']), 2)
        self.assertIn('e01', results[0]['edge_bindings'])
        self.assertIn('e02', results[0]['edge_bindings'])

        self.assertEqual(len(results[1]['node_bindings']), 3)
        self.assertIn('n1', results[1]['node_bindings'])
        self.assertIn('n2', results[1]['node_bindings'])
        self.assertIn('n4', results[1]['node_bindings'])

        self.assertEqual(len(results[1]['edge_bindings']), 2)
        self.assertIn('e01', results[1]['edge_bindings'])
        self.assertIn('e03', results[1]['edge_bindings'])
