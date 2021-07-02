import unittest
from biothings_explorer.query_graph_handler.query_node import QNode


class TestQueryNodeModule(unittest.TestCase):
    node1_equivalent_ids = {
        'NCBIGene:1017': {
            'db_ids': {
                'NCBIGene': ["1017"],
                'SYMBOL': ['CDK2']
            }
        }
    }

    def test_has_input_function_node_without_curies_specified_should_return_false(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        res = gene_node.has_input()
        self.assertFalse(res)

    def test_has_input_function_node_with_curies_specified_should_return_true(self):
        gene_node = QNode('n1', {'categories': 'Gene', 'ids': 'NCBIGene:1017'})
        res = gene_node.has_input()
        self.assertTrue(res)

    def test_has_equivalent_ids_node_with_equivalent_identifiers_set_should_return_true(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        gene_node.set_equivalent_ids(self.node1_equivalent_ids)
        res = gene_node.has_equivalent_ids()
        self.assertTrue(res)

    def test_has_equivalent_ids_node_with_equivalent_identifiers_not_set_should_return_false(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        res = gene_node.has_equivalent_ids()
        self.assertFalse(res)

    def test_get_entities_if_equivalent_ids_are_empty_should_return_an_empty_array(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        gene_node.equivalent_ids = {}
        self.assertEqual(gene_node.get_entities(), [])

    def test_get_entities_if_equivalent_ids_are_not_empty_should_return_an_array_of_bioentities(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        gene_node.equivalent_ids = {
            'A': [
                {
                    'a': 'b'
                },
                {
                    'c': 'd'
                }
            ],
            'B': [
                {
                    'e': 'f'
                }
            ]
        }
        self.assertEqual(gene_node.get_entities(), [
                {
                    "a": "b"
                },
                {
                    "c": "d"
                },
                {
                    "e": "f"
                }
            ])

    def test_get_primary_ids_if_equivalent_ids_are_empty_should_return_an_empty_array(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        gene_node.equivalent_ids = {}
        self.assertEqual(gene_node.get_primary_ids(), [])

    def test_get_primary_ids_if_equivalent_ids_are_not_empty_should_return_an_array_of_primary_ids(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        gene_node.equivalent_ids = {
            "A": [
                {
                    "primaryID": "b"
                },
                {
                    "primaryID": "c"
                }
            ],
            "B": [
                {
                    "primaryID": "d"
                }
            ]
        }
        self.assertEqual(gene_node.get_primary_ids(), ['b', 'c', 'd'])

    def test_update_equivalent_ids_if_equivalent_ids_does_not_exist_should_set_it_with_the_input(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        gene_node.update_equivalent_ids({'a': 'b'})
        self.assertEqual(gene_node.equivalent_ids, {'a': 'b'})

    def test_update_equivalent_ids_if_equivalent_ids_are_not_empty_should_update_the_equivalent_ids(self):
        gene_node = QNode('n1', {'categories': 'Gene'})
        gene_node.equivalent_ids = {'a': 'b', 'c': 'd'}
        gene_node.update_equivalent_ids({'e': 'f'})
        self.assertEqual(gene_node.get_equivalent_ids(), { "a": "b", "c": "d", "e": "f" })

    def test_get_categories_if_equivalent_ids_are_empty_return_itself_and_its_descendants(self):
        node = QNode('n1', {'categories': 'DiseaseOrPhenotypicFeature'})
        self.assertIn('Disease', node.get_categories())
        self.assertIn('PhenotypicFeature', node.get_categories())
        self.assertIn('DiseaseOrPhenotypicFeature', node.get_categories())

    def test_get_categories_if_equivalent_ids_are_empty_return_itself_and_its_descendants_using_namedthing_as_example(self):
        node = QNode('n1', {'categories': 'NamedThing'})
        self.assertIn('Disease', node.get_categories())
        self.assertIn('PhenotypicFeature', node.get_categories())
        self.assertIn('DiseaseOrPhenotypicFeature', node.get_categories())
        self.assertIn('Gene', node.get_categories())
        self.assertIn('NamedThing', node.get_categories())

    def test_get_categories_if_equivalent_ids_are_empty_return_itself_and_its_descendants_using_gene_as_example(self):
        node = QNode('n1', {'categories': 'Gene'})
        self.assertEqual(node.get_categories(), ['Gene'])

    def test_get_categories_if_equivalent_ids_are_not_empty_return_all_semantic_types_defined_in_the_entity(self):
        node = QNode('n1', {'categories': 'Gene'})
        node.equivalent_ids = {
            "A": [
                {
                    "semanticTypes": ["m", "n"]
                },
                {
                    "semanticTypes": ["p", "q"]
                }
            ],
            "B": [
                {
                    "semanticTypes": ["x", "y"]
                }
            ]
        }
        self.assertEqual(node.get_categories(), ["m", "n", "p", "q", "x", "y"])

    