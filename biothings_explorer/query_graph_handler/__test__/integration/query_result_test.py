import copy
import unittest
from biothings_explorer.query_graph_handler.query_node import QNode
from biothings_explorer.query_graph_handler.query_edge import QEdge
from biothings_explorer.query_graph_handler.query_results import QueryResult


class TestQueryResults(unittest.TestCase):
    def test_single_record_should_get_n1_n2_and_e01(self):
        gene_node1 = QNode('n1', {'categories': ['Gene'], 'ids': ['NCBIGene:632']})
        chemical_node1 = QNode('n2', {'categories': ['ChemicalSubstance']})
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
        self.assertIn('e01', query_result.get_results()[0]['edge_bindings'])
        self.assertIn('score', query_result.get_results()[0])

    def test_two_records_query_graph_gene1_disease1_gene1(self):
        gene_node_start = QNode('n1', {'categories': ['Gene']})
        disease_node = QNode('n2', {'categories': ['Disease']})
        gene_node_end = QNode('n3', {'categories': ['Gene']})
        edge1 = QEdge('e01', {'subject': gene_node_start, 'object': disease_node})
        edge2 = QEdge('e02', {'subject': disease_node, 'object': gene_node_end})

        record1 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge1,
                'predicate': 'biolink:gene_associated_with_condition',
                'api_name': 'Automat Pharos',
            },
            'publications': ['PMID:123', 'PMID:1234'],
            '$input': {
                'original': 'SYMBOL:KCNMA1',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:3778',
                        'label': 'KCNMA1',
                        'dbIDs': {
                            'SYMBOL': 'KCNMA1',
                            'NCBIGene': '3778',
                        },
                        'curies': ['SYMBOL:KCNMA1', 'NCBIGene:3778'],
                    },
                ],
            },
            '$output': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
        }

        record2 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge2,
                'predicate': 'biolink:condition_associated_with_gene',
                'api_name': 'Automat Hetio',
            },
            'publications': ['PMID:345', 'PMID:456'],
            '$input': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
            '$output': {
                'original': 'SYMBOL:KCNMA1',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:3778',
                        'label': 'KCNMA1',
                        'dbIDs': {
                            'SYMBOL': 'KCNMA1',
                            'NCBIGene': '3778',
                        },
                        'curies': ['SYMBOL:KCNMA1', 'NCBIGene:3778'],
                    },
                ],
            },
        }

        query_result = QueryResult()
        query_result.update({
            'e01': {
                'connected_to': ['e02'],
                'records': [record1]
            },
            'e02': {
                'connected_to': ['e01'],
                'records': [record2]
            }
        })

        results = query_result.get_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]['node_bindings']), 3)
        self.assertIn('n1', results[0]['node_bindings'])
        self.assertIn('n2', results[0]['node_bindings'])
        self.assertIn('n3', results[0]['node_bindings'])

        self.assertEqual(len(results[0]['edge_bindings']), 2)
        self.assertIn('e01', results[0]['edge_bindings'])
        self.assertIn('e02', results[0]['edge_bindings'])
        self.assertIn('score', results[0])

    def test_query_graph_gene1_disease1_gene2_no_ids_params(self):
        gene_node_start = QNode('n1', {'categories': ['Gene']})
        disease_node = QNode('n2', {'categories': ['Disease']})
        gene_node_end = QNode('n3', {'categories': ['Gene']})
        edge1 = QEdge('e01', {'subject': gene_node_start, 'object': disease_node})
        edge2 = QEdge('e02', {'subject': disease_node, 'object':gene_node_end})

        record1 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge1,
                'predicate': 'biolink:gene_associated_with_condition',
                'api_name': 'Automat Pharos',
            },
            'publications': ['PMID:123', 'PMID:1234'],
            '$input': {
                'original': 'SYMBOL:KCNMA1',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:3778',
                        'label': 'KCNMA1',
                        'dbIDs': {
                            'SYMBOL': 'KCNMA1',
                            'NCBIGene': '3778',
                        },
                        'curies': ['SYMBOL:KCNMA1', 'NCBIGene:3778'],
                    },
                ],
            },
            '$output': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
        }

        record2 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge2,
                'predicate': 'biolink:condition_associated_with_gene',
                'api_name': 'Automat Hetio',
            },
            'publications': ['PMID:345', 'PMID:456'],
            '$input': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
            '$output': {
                'original': 'SYMBOL:TULP3',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:7289',
                        'label': 'TULP3',
                        'dbIDs': {
                            'SYMBOL': 'TULP3',
                            'NCBIGene': '7289',
                        },
                        'curies': ['SYMBOL:TULP3', 'NCBIGene:7289'],
                    },
                ],
            },
        }

        query_result = QueryResult()
        query_result.update({
            'e01': {
                'connected_to': ['e02'],
                'records': [record1]
            },
            'e02': {
                'connected_to': ['e01'],
                'records': [record2]
            }
        })

        results = query_result.get_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]['node_bindings']), 3)
        self.assertIn('n1', results[0]['node_bindings'])
        self.assertIn('n2', results[0]['node_bindings'])
        self.assertIn('n3', results[0]['node_bindings'])

        self.assertEqual(len(results[0]['edge_bindings']), 2)
        self.assertIn('e01', results[0]['edge_bindings'])
        self.assertIn('e02', results[0]['edge_bindings'])

        self.assertIn('score', results[0])

    def test_query_graph_gene1_disease1_gene2_gene1_has_ids_params(self):
        gene_node_start = QNode('n1', {'categories': ['Gene'], 'ids': ['NCBIGene:3778']})
        disease_node = QNode('n2', {'categories': ['Disease']})
        gene_node_end = QNode('n3', {'categories': ['Gene']})

        edge1 = QEdge('e01', {'subject': gene_node_start, 'object': disease_node})
        edge2 = QEdge('e02', {'subject': disease_node, 'object': gene_node_end})

        record1 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge1,
                'predicate': 'biolink:gene_associated_with_condition',
                'api_name': 'Automat Pharos',
            },
            'publications': ['PMID:123', 'PMID:1234'],
            '$input': {
                'original': 'SYMBOL:KCNMA1',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:3778',
                        'label': 'KCNMA1',
                        'dbIDs': {
                            'SYMBOL': 'KCNMA1',
                            'NCBIGene': '3778',
                        },
                        'curies': ['SYMBOL:KCNMA1', 'NCBIGene:3778'],
                    },
                ],
            },
            '$output': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
        }

        record2 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge2,
                'predicate': 'biolink:condition_associated_with_gene',
                'api_name': 'Automat Hetio',
            },
            'publications': ['PMID:345', 'PMID:456'],
            '$input': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
            '$output': {
                'original': 'SYMBOL:TULP3',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:7289',
                        'label': 'TULP3',
                        'dbIDs': {
                            'SYMBOL': 'TULP3',
                            'NCBIGene': '7289',
                        },
                        'curies': ['SYMBOL:TULP3', 'NCBIGene:7289'],
                    },
                ],
            },
        }

        query_result = QueryResult()
        query_result.update({
            'e01': {
                'connected_to': ['e02'],
                'records': [record1]
            },
            'e02': {
                'connected_to': ['e01'],
                'records': [record2]
            }
        })

        results = query_result.get_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]['node_bindings']), 3)
        self.assertIn('n1', results[0]['node_bindings'])
        self.assertIn('n2', results[0]['node_bindings'])
        self.assertIn('n3', results[0]['node_bindings'])

        self.assertEqual(len(results[0]['edge_bindings']), 2)
        self.assertIn('e01', results[0]['edge_bindings'])
        self.assertIn('e02', results[0]['edge_bindings'])

        self.assertIn('score', results[0])

    def test_query_graph_gene1_disease1_gene2_gene1_and_gene2_have_ids_params(self):
        gene_node_start = QNode('n1', {'categories': ['Gene'], 'ids': ['NCBIGene:3778']})
        disease_node = QNode('n2', {'categories': ['Disease']})
        gene_node_end = QNode('n3', {'categories': ['Gene'], 'ids': ['NCBIGene:7289']})

        edge1 = QEdge('e01', {'subject': gene_node_start, 'object': disease_node})
        edge2 = QEdge('e02', {'subject': disease_node, 'object': gene_node_end})

        record1 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge1,
                'predicate': 'biolink:gene_associated_with_condition',
                'api_name': 'Automat Pharos',
            },
            'publications': ['PMID:123', 'PMID:1234'],
            '$input': {
                'original': 'SYMBOL:KCNMA1',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:3778',
                        'label': 'KCNMA1',
                        'dbIDs': {
                            'SYMBOL': 'KCNMA1',
                            'NCBIGene': '3778',
                        },
                        'curies': ['SYMBOL:KCNMA1', 'NCBIGene:3778'],
                    },
                ],
            },
            '$output': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
        }

        record2 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge2,
                'predicate': 'biolink:condition_associated_with_gene',
                'api_name': 'Automat Hetio',
            },
            'publications': ['PMID:345', 'PMID:456'],
            '$input': {
                'original': 'SYMBOL:TULP3',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:7289',
                        'label': 'TULP3',
                        'dbIDs': {
                            'SYMBOL': 'TULP3',
                            'NCBIGene': '7289',
                        },
                        'curies': ['SYMBOL:TULP3', 'NCBIGene:7289'],
                    },
                ],
            },
            '$output': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
        }

        query_result = QueryResult()
        query_result.update({
            'e01': {
                'connected_to': ['e02'],
                'records': [record1]
            },
            'e02': {
                'connected_to': ['e02'],
                'records': [record2]
            }
        })

        results = query_result.get_results()
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]['node_bindings']), 3)
        self.assertIn('n1', results[0]['node_bindings'])
        self.assertIn('n2', results[0]['node_bindings'])
        self.assertIn('n3', results[0]['node_bindings'])

        self.assertEqual(len(results[0]['edge_bindings']), 2)
        self.assertIn('e01', results[0]['edge_bindings'])
        self.assertIn('e02', results[0]['edge_bindings'])

        self.assertIn('score', results[0])

    def test_query_graph_gene1_disease1_gene2_gene2_has_ids_param(self):
        gene_node_start = QNode('n1', {'categories': ['Gene']})
        disease_node = QNode('n2', {'categories': ['Disease']})
        gene_node_end = QNode('n3', {'categories': ['Gene'], 'ids': ['NCBIGene:7289']})

        edge1 = QEdge('e01', {'subject': gene_node_start, 'object': disease_node})
        edge2 = QEdge('e02', {'subject': disease_node, 'object': gene_node_end})

        record1 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge1,
                'predicate': 'biolink:gene_associated_with_condition',
                'api_name': 'Automat Pharos',
            },
            'publications': ['PMID:123', 'PMID:1234'],
            '$input': {
                'original': 'SYMBOL:KCNMA1',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:3778',
                        'label': 'KCNMA1',
                        'dbIDs': {
                            'SYMBOL': 'KCNMA1',
                            'NCBIGene': '3778',
                        },
                        'curies': ['SYMBOL:KCNMA1', 'NCBIGene:3778'],
                    },
                ],
            },
            '$output': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
        }

        record2 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge2,
                'predicate': 'biolink:condition_associated_with_gene',
                'api_name': 'Automat Hetio',
            },
            'publications': ['PMID:345', 'PMID:456'],
            '$input': {
                'original': 'SYMBOL:TULP3',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:7289',
                        'label': 'TULP3',
                        'dbIDs': {
                            'SYMBOL': 'TULP3',
                            'NCBIGene': '7289',
                        },
                        'curies': ['SYMBOL:TULP3', 'NCBIGene:7289'],
                    },
                ],
            },
            '$output': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
        }

        query_result = QueryResult()
        query_result.update({
            'e01': {
                'connected_to': ['e02'],
                'records': [record1]
            },
            'e02': {
                'connected_to': ['e01'],
                'records': [record2]
            }
        })

        results = query_result.get_results()

        self.assertEqual(len(results), 1)

        self.assertEqual(len(results[0]['node_bindings']), 3)
        self.assertIn('n1', results[0]['node_bindings'])
        self.assertIn('n2', results[0]['node_bindings'])
        self.assertIn('n3', results[0]['node_bindings'])

        self.assertEqual(len(results[0]['edge_bindings']), 2)
        self.assertIn('e01', results[0]['edge_bindings'])
        self.assertIn('e02', results[0]['edge_bindings'])

        self.assertIn('score', results[0])

    def test_three_records_should_get_2_results_when_query_graph_is_dashdash_and_records_are_dashlessthan(self):
        gene_node_start = QNode('n1', {'categories': ['Gene'], 'ids': ['NCBIGene:3778']})
        disease_node = QNode('n2', {'categories': ['Disease']})
        gene_node_end = QNode('n3', {'categories': ['Gene']})

        edge1 = QEdge('e01', {'subject': gene_node_start, 'object': disease_node})
        edge2 = QEdge('e02', {'subject': disease_node, 'object': gene_node_end})

        record1 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge1,
                'predicate': 'biolink:gene_associated_with_condition',
                'api_name': 'Automat Pharos',
            },
            'publications': ['PMID:123', 'PMID:1234'],
            '$input': {
                'original': 'SYMBOL:KCNMA1',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:3778',
                        'label': 'KCNMA1',
                        'dbIDs': {
                            'SYMBOL': 'KCNMA1',
                            'NCBIGene': '3778',
                        },
                        'curies': ['SYMBOL:KCNMA1', 'NCBIGene:3778'],
                    },
                ],
            },
            '$output': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
        }

        record2 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge2,
                'predicate': 'biolink:condition_associated_with_gene',
                'api_name': 'Automat Hetio',
            },
            'publications': ['PMID:345', 'PMID:456'],
            '$input': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
            '$output': {
                'original': 'SYMBOL:TULP3',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:7289',
                        'label': 'TULP3',
                        'dbIDs': {
                            'SYMBOL': 'TULP3',
                            'NCBIGene': '7289',
                        },
                        'curies': ['SYMBOL:TULP3', 'NCBIGene:7289'],
                    },
                ],
            },
        }

        record3 = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge2,
                'predicate': 'biolink:condition_associated_with_gene',
                'api_name': 'Automat Hetio',
            },
            'publications': ['PMID:987', 'PMID:876'],
            '$input': {
                'original': 'MONDO:0011122',
                'obj': [
                    {
                        'primaryID': 'MONDO:0011122',
                        'label': 'obesity disorder',
                        'dbIDs': {
                            'MONDO': '0011122',
                            'MESH': 'D009765',
                            'name': 'obesity disorder',
                        },
                        'curies': ['MONDO:0011122', 'MESH:D009765', 'name:obesity disorder'],
                    },
                ],
            },
            '$output': {
                'original': 'SYMBOL:TECR',
                'obj': [
                    {
                        'primaryID': 'NCBIGene:9524',
                        'label': 'TECR',
                        'dbIDs': {
                            'SYMBOL': 'TECR',
                            'NCBIGene': '9524',
                        },
                        'curies': ['SYMBOL:TECR', 'NCBIGene:9524'],
                    },
                ],
            },
        }

        query_result = QueryResult()

        query_result.update({
            'e01': {
                'connected_to': ['e02'],
                'records': [record1]
            },
            'e02': {
                'connected_to': ['e01'],
                'records': [record2, record3]
            }
        })

        results = query_result.get_results()

        self.assertEqual(len(results), 2)

        self.assertEqual(len(results[0]['node_bindings']), 3)
        self.assertIn('n1', results[0]['node_bindings'])
        self.assertIn('n2', results[0]['node_bindings'])
        self.assertIn('n3', results[0]['node_bindings'])

        self.assertEqual(len(results[0]['edge_bindings']), 2)
        self.assertIn('e01', results[0]['edge_bindings'])
        self.assertIn('e02', results[0]['edge_bindings'])

        self.assertIn('score', results[0])

        self.assertEqual(len(results[1]['node_bindings']), 3)
        self.assertIn('n1', results[1]['node_bindings'])
        self.assertIn('n2', results[1]['node_bindings'])
        self.assertIn('n3', results[1]['node_bindings'])

        self.assertEqual(len(results[1]['edge_bindings']), 2)
        self.assertIn('e01', results[1]['edge_bindings'])
        self.assertIn('e02', results[1]['edge_bindings'])

        self.assertIn('score', results[1])

    def test_synthetic_records(self):
        n0 = QNode('n0', {'categories': ['category_n0_n2'], 'ids': ['n0a']})
        n1 = QNode('n1', {'categories': ['category_n1']})
        n2 = QNode('n2', {'categories': ['category_n0_n2']})
        n3 = QNode('n3', {'categories': ['biolink:category_n3']})
        n4 = QNode('n4', {'categories': ['category_n4']})
        n5 = QNode('n5', {'categories': ['category_n5']})

        e0 = QEdge('e0', {'subject': n0, 'object': n1})

        e1 = QEdge('e1', {'subject': n1, 'object': n2})
        e2 = QEdge('e2', {'subject': n1, 'object': n3})
        e3 = QEdge('e3', {'subject': n1, 'object': n4})

        e4 = QEdge('e4', {'subject': n2, 'object': n5})
        e5 = QEdge('e5', {'subject': n3, 'object': n5})
        e6 = QEdge('e6', {'subject': n4, 'object': n5})

        record0_n0a_n1a = {
            '$edge_metadata': {
                'trapi_qEdge_obj': e0,
                'predicate': 'biolink:record0_pred0',
                'source': 'source0',
                'api_name': 'api0',
            },
            # n0
            '$input': {
                'obj': [
                    {
                        'primaryID': 'n0a',
                    },
                ],
            },
            # n1
            '$output': {
                'obj': [
                    {
                        'primaryID': 'n1a',
                    },
                ],
            },
        }

        record0_n0a_n1a_pred0_api1 = copy.deepcopy(record0_n0a_n1a)
        record0_n0a_n1a_pred0_api1['$edge_metadata']['source'] = 'source1'
        record0_n0a_n1a_pred0_api1['$edge_metadata']['api_name'] = 'api1'

        record0_n0a_n1a_pred1_api0 = copy.deepcopy(record0_n0a_n1a)
        record0_n0a_n1a_pred1_api0['$edge_metadata']['predicate'] = 'biolink:record0_pred1'

        record0_n0a_n1a_pred1_api1 = copy.deepcopy(record0_n0a_n1a)
        record0_n0a_n1a_pred1_api1['$edge_metadata']['predicate'] = 'biolink:record0_pred1'
        record0_n0a_n1a_pred1_api1['$edge_metadata']['source'] = 'source1'
        record0_n0a_n1a_pred1_api1['$edge_metadata']['api_name'] = 'api1'
