import unittest
from biothings_explorer.bte_trapi_query_graph_handler.query_node import QNode
from biothings_explorer.bte_trapi_query_graph_handler.query_edge import QEdge


class TestingQueryEdgeModule(unittest.TestCase):
    gene_node1 = QNode('n1', {'categories': 'Gene', 'ids': 'NCBIGene:1017'})
    type_node = QNode('n2', {'categories': 'ChemicalSubstance'})
    disease1_node = QNode('n1', {'categories': 'Disease', 'ids': 'MONDO:000123'})
    node1_equivalent_ids = {
        'NCBIGene:1017': {
            'db_ids': {
                'NCBIGene': ["1017"],
                'SYMBOL': ['CDK2']
            }
        }
    }

    gene_node2 = QNode('n2', {'categories': 'Gene', 'ids': ["NCBIGene:1017", "NCBIGene:1018"]})
    gene_node1_with_id_annotated = QNode('n1', {'categories': 'Gene', 'ids': 'NCBIGene:1017'})
    gene_node1_with_id_annotated.set_equivalent_ids(node1_equivalent_ids)
    invalid_node = QNode('n3', {'categories': 'INVALID', 'curie': ["NCBIGene:1017", "NCBIGene:1018"]})
    chemical_node1 = QNode('n3', {'categories': 'ChemicalSubstance'})
    edge1 = QEdge('e01', {'subject': gene_node1, 'object': chemical_node1})
    edge2 = QEdge('e02', {'subject': gene_node1_with_id_annotated, 'object': chemical_node1})
    edge3 = QEdge('e04', {'subject': gene_node2, 'object': chemical_node1})
    edge4 = QEdge('e05', {'object': gene_node2, 'subject': chemical_node1})
    edge5 = QEdge('e06', {'object': gene_node1_with_id_annotated, 'subject': chemical_node1})

    def test_is_reversed_if_only_the_object_of_the_edge_has_curie_defined_should_return_true(self):
        res = self.edge4.is_reversed()
        self.assertTrue(res)

    def test_is_reversed_if_the_subject_of_the_edge_has_curie_defined_should_return_false(self):
        res = self.edge1.is_reversed()
        self.assertFalse(res)

    def test_is_reversed_if_both_subject_and_object_curie_not_defined_should_return_false(self):
        node1 = QNode('n1', {'categories': 'Gene'})
        node2 = QNode('n2', {'categories': 'ChemicalSubstance'})
        edge = QEdge('e01', {'subject': node1, 'object': node2})
        self.assertFalse(edge.is_reversed())

    def test_get_input_curie_return_an_array_of_one_curie_if_subject_has_only_one_curie_specified(self):
        res = self.edge1.get_input_curie()
        self.assertEqual(res, ['NCBIGene:1017'])

    def test_get_input_curie_return_an_array_of_two_curie_if_subject_has_only_an_array_of_two_curies_specified(self):
        res = self.edge3.get_input_curie()
        self.assertEqual(res, ['NCBIGene:1017', 'NCBIGene:1018'])

    def test_get_input_curie_return_an_array_of_two_curies_if_edge_is_reversed_and_object_has_two_curies_specified(self):
        res = self.edge4.get_input_curie()
        self.assertEqual(res, ['NCBIGene:1017', 'NCBIGene:1018'])

    def test_has_input_return_true_if_subject_has_only_one_curie_specified(self):
        res = self.edge1.has_input()
        self.assertTrue(res)

    def test_has_input_return_true_if_subject_has_only_an_array_of_two_curies_specified(self):
        res = self.edge3.has_input()
        self.assertTrue(res)

    def test_has_input_return_true_if_subject_has_no_curies_specified_but_object_does(self):
        res = self.edge4.has_input()
        self.assertTrue(res)

    def test_has_input_return_false_if_both_subject_and_object_has_no_curies_specified(self):
        node1 = QNode('n1', {'categories': 'Gene'})
        node2 = QNode('n2', {'categories': 'ChemicalSubstance'})
        edge = QEdge('e01', {'subject': node1, 'object': node2})
        self.assertFalse(edge.has_input())

    def test_has_input_resolved_return_true_if_subject_has_input_resolved(self):
        res = self.edge2.has_input_resolved()
        self.assertTrue(res)

    def test_has_input_resolved_return_false_if_both_subject_and_object_do_not_have_input_resolved(self):
        res = self.edge1.has_input_resolved()
        self.assertFalse(res)

    def test_has_input_resolved_return_true_if_subject_doesnt_have_input_resolved_but_object_does(self):
        res = self.edge5.has_input_resolved()
        self.assertTrue(res)

    def test_get_predicate_get_reverse_predicate_if_query_is_reversed(self):
        edge = QEdge('e01', {'subject': self.type_node, 'object': self.disease1_node, 'predicates': 'biolink:treats'})
        res = edge.get_predicate()
        self.assertIn('treated_by', res)

    def test_get_predicate_get_reverse_if_query_is_reversed_and_expanded(self):
        edge = QEdge('e01', {'subject': self.type_node, 'object': self.disease1_node, 'predicates': 'biolink:affects'})
        res = edge.get_predicate()
        self.assertIn('affected_by', res)
        self.assertIn('disrupted_by', res)

    def test_expand_predicates_all_predicates_are_correctly_expanded_if_in_biolink_model(self):
        edge = QEdge('e01', {'subject': self.type_node, 'object': self.disease1_node, 'predicates': 'biolink:contributes_to'})
        res = edge.expand_predicates(['contributes_to'])
        self.assertIn('contributes_to', res)
        self.assertIn('causes', res)

    def test_expand_predicates_multiple_predicates_can_be_resolved(self):
        edge = QEdge('e01', {'subject': self.type_node, 'object': self.disease1_node, 'predicates': 'biolink:contributes_to'})
        res = edge.expand_predicates(["contributes_to", "ameliorates"])
        self.assertIn('contributes_to', res)
        self.assertIn('causes', res)
        self.assertIn('ameliorates', res)
        self.assertIn('treats', res)

    def test_expand_predicates_predicates_not_in_biolink_model_should_return_itself(self):
        edge = QEdge('e01', {'subject': self.type_node, 'object': self.disease1_node, 'predicates': 'biolink:contributes_to'})
        res = edge.expand_predicates(["contributes_to", "amelio"])
        self.assertIn('contributes_to', res)
        self.assertIn('causes', res)
        self.assertIn('amelio', res)
