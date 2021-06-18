import unittest
from biothings_explorer.bte_trapi_query_graph_handler.query_graph import QueryGraphHandler
from biothings_explorer.bte_trapi_query_graph_handler.query_node import QNode
from biothings_explorer.bte_trapi_query_graph_handler.query_edge import QEdge
from biothings_explorer.bte_trapi_query_graph_handler.exceptions.invalid_query_graph_error import InvalidQueryGraphError


class TestQueryGraphHandler(unittest.TestCase):
    disease_entity_node = {
        'categories': 'biolink:Disease',
        'ids': 'MONDO:0005737'
    }

    gene_entity_node = {
        'categories': 'biolink:Gene',
        'ids': 'NCBIGene:1017'
    }

    gene_class_node = {
        'categories': 'biolink:Gene'
    }

    chemical_class_node = {
        'categories': 'biolink:ChemicalSubstance'
    }

    pathway_class_node = {
        'categories': 'biolink:Pathways'
    }

    phenotype_class_node = {
        'categories': 'biolink:Phenotype'
    }

    OneHopQuery = {
        "nodes": {
            "n0": disease_entity_node,
            "n1": gene_class_node
        },
        "edges": {
            "e01": {
                "subject": "n0",
                "object": "n1"
            }
        }
    }

    ThreeHopExplainQuery = {
        "nodes": {
            "n0": disease_entity_node,
            "n1": gene_class_node,
            "n2": chemical_class_node,
            "n3": gene_entity_node,
        },
        "edges": {
            "e01": {
                "subject": "n0",
                "object": "n1"
            },
            "e02": {
                "subject": "n1",
                "object": "n2"
            },
            "e03": {
                "subject": "n2",
                "object": "n3"
            }
        }
    }

    FourHopQuery = {
        "nodes": {
            "n0": disease_entity_node,
            "n1": gene_class_node,
            "n2": chemical_class_node,
            "n3": phenotype_class_node,
            "n4": pathway_class_node,
        },
        "edges": {
            "e01": {
                "subject": "n0",
                "object": "n1"
            },
            "e02": {
                "subject": "n1",
                "object": "n2"
            },
            "e03": {
                "subject": "n2",
                "object": "n3"
            },
            "e04": {
                "subject": "n3",
                "object": "n4"
            },
        }
    }

    def test_store_nodes_if_store_nodes_with_one_hop_query(self):
        handler = QueryGraphHandler(self.OneHopQuery)
        nodes = handler._store_nodes()
        self.assertIn('n0', nodes)
        self.assertNotIn('n2', nodes)
        self.assertIsInstance(nodes['n0'], QNode)

    def test_store_nodes_with_multi_hop_query(self):
        handler = QueryGraphHandler(self.FourHopQuery)
        nodes = handler._store_nodes()
        self.assertIn('n0', nodes)
        self.assertIn('n3', nodes)
        self.assertIsInstance(nodes['n0'], QNode)
        self.assertIsInstance(nodes['n3'], QNode)

    def test_store_edges_with_one_hop_query(self):
        handler = QueryGraphHandler(self.OneHopQuery)
        edges = handler._store_edges()
        self.assertIn('e01', edges)
        self.assertNotIn('e02', edges)
        self.assertIsInstance(edges['e01'], QEdge)
        self.assertIsInstance(edges['e01'].get_subject(), QNode)

    def test_store_edges_with_multi_hop_query(self):
        handler = QueryGraphHandler(self.FourHopQuery)
        edges = handler._store_edges()
        self.assertIn('e01', edges)
        self.assertIn('e02', edges)
        self.assertIsInstance(edges['e01'], QEdge)

    def test_create_query_paths_with_three_hop_explain_query(self):
        handler = QueryGraphHandler(self.ThreeHopExplainQuery)
        edges = handler.create_query_paths()
        self.assertEqual(len(edges), 3)
        self.assertEqual(len(edges[0]), 2)
        self.assertEqual(len(edges[1]), 2)
        self.assertEqual(len(edges[2]), 2)
