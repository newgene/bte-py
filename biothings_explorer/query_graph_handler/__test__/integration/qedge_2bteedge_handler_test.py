import unittest
from biothings_explorer.query_graph_handler.query_node import QNode
from biothings_explorer.query_graph_handler.query_edge import QEdge
from biothings_explorer.query_graph_handler.update_nodes import NodesUpdateHandler


class TestNodeUpdateHandler(unittest.TestCase):
    gene_node1 = QNode('n1', {'categories': ['Gene'], 'ids': ['NCBIGene:1017']})
    node1_equivalent_ids = {
        'db_ids': {
            'NCBIGene': ["1017"],
            'SYMBOL': ['CDK2']
        }
    }

    gene_node2 = QNode('n2', {'categories': ['Gene'], 'ids': ["NCBIGene:1017", "NCBIGene:1018"]})
    gene_node1_with_id_annotated = QNode('n1', {'categories': ['Gene'], 'ids': ["NCBIGene:1017"]})
    gene_node1_with_id_annotated.set_equivalent_ids(node1_equivalent_ids)
    chemical_node1 = QNode('n3', {'categories': ['SmallMolecule']})
    edge1 = QEdge('e01', {'subject': gene_node1, 'object': chemical_node1})
    edge2 = QEdge('e02', {'subject': gene_node1_with_id_annotated, 'object': chemical_node1})
    edge3 = QEdge('e04', {'subject': gene_node2, 'object': chemical_node1})
    edge4 = QEdge('e05', {'subject': gene_node2, 'object': chemical_node1})

    def test_get_curies_edge_with_one_curie_input_return_an_array_of_one(self):
        node_updater = NodesUpdateHandler([self.edge1])
        res = node_updater._get_curies([self.edge1])
        self.assertIn('Gene', res)
        self.assertEqual(res['Gene'], ["NCBIGene:1017"])

    def test_get_curies_edge_with_multiple_curie_input_return_an_array_with_multiple_items(self):
        node_updater = NodesUpdateHandler([self.edge3])
        res = node_updater._get_curies([self.edge3])
        self.assertEqual(len(res['Gene']), 2)

    def test_get_curies_edge_with_input_node_annotated_should_return_an_empty_array(self):
        node_updater = NodesUpdateHandler([self.edge2])
        res = node_updater._get_curies([self.edge2])
        self.assertEqual(res, {})

    def test_get_curies_edge_with_input_on_object_end_should_be_handled(self):
        node_updater = NodesUpdateHandler([self.edge4])
        res = node_updater._get_curies([self.edge4])
        self.assertEqual(len(res['Gene']), 2)

    def test_get_equivalent_ids_edge_with_one_curie_input_return_an_object_with_one_key(self):
        node_updater = NodesUpdateHandler([self.edge1])
        res = node_updater._get_equivalent_ids({'Gene': ["NCBIGene:1017"]})
        self.assertIn('NCBIGene:1017', res)

    def test_get_equivalent_ids_edge_with_multiple_curie_input_return_an_object_with_multiple_key(self):
        node_updater = NodesUpdateHandler([self.edge1])
        res = node_updater._get_equivalent_ids({'Gene': ["NCBIGene:1017", "NCBIGene:1018"], 'SmallMolecule': ["PUBCHEM:5070"]})
        self.assertIn('NCBIGene:1017', res)
        self.assertIn('NCBIGene:1018', res)
        self.assertIn('PUBCHEM:5070', res)