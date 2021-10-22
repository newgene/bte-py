import os
import unittest
from biothings_explorer.biolink_model.tree.slot_tree import BioLinkClassTree as BioLinkSlotTree
from biothings_explorer.biolink_model.object.slot_object import Slot
from biothings_explorer.biolink_model.exceptions.node_not_found import NodeNotFound
import yaml


class TestConstructFunction(unittest.TestCase):
    tree = {}
    objs = {}

    def setUp(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        with open(file_path, encoding="utf8") as f:
            jsonObj = yaml.load(f)
            self.objs = jsonObj.get('slots')
            self.tree = BioLinkSlotTree(self.objs)

    def test_all_objects_are_correctly_loaded(self):
        self.tree.construct()
        self.assertIn('negatively_regulates', self.tree.objects)
        self.assertIsInstance(self.tree.objects['negatively_regulates'], Slot)
        self.assertIn('positively_regulates', self.tree.objects)
        self.assertIn('disrupts', self.tree.objects)
        self.assertEqual(len(self.tree.objects.keys()), len(self.objs.keys()))

    def test_hierarchical_order_are_correctly_passed(self):
        self.tree.construct()
        self.assertIn('negatively_regulates', self.tree.objects['regulates'].children)
        self.assertIn('disrupted_by', self.tree.objects['affected_by'].children)
        self.assertNotIn('negatively_regulates', self.tree.objects['affected_by'].children)
        self.assertEqual(len(self.tree.objects['negatively_regulates'].children), 2)
        self.assertEqual(self.tree.objects['negatively_regulates'].children, [
            'process_negatively_regulates_process',
            'entity_negatively_regulates_entity',
        ])

    def test_non_explicit_inverses_are_correctly_inferred(self):
        self.tree.construct()
        self.assertEqual('condition_associated_with_gene', self.tree.objects['gene_associated_with_condition'].inverse)
        self.assertEqual('approved_for_treatment_by', self.tree.objects['approved_to_treat'].inverse)
        self.assertEqual('has_catalyst', self.tree.objects['catalyzes'].inverse)


class TestGetDescendantsFunction(unittest.TestCase):
    tree = {}

    def setUp(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        with open(file_path, encoding="utf8") as f:
            jsonObj = yaml.load(f)
            self.objs = jsonObj.get('slots')
            self.tree = BioLinkSlotTree(self.objs)
            self.tree.construct()

    def test_multi_level_inheritancy_is_correctly_passed(self):
        self.assertIn(self.tree.objects['superclass_of'], self.tree.get_descendants('related_to'))
        self.assertNotIn(self.tree.objects['related_to'], self.tree.get_descendants('superclass_of'))

    def test_entity_without_descendants_should_return_empty_array(self):
        self.assertEqual(len(self.tree.get_descendants('process_positively_regulated_by_process')), 0)
        self.assertEqual(len(self.tree.get_descendants('superclass_of')), 0)

    def test_entity_not_in_the_tree_should_throw_an_error(self):
        with self.assertRaises(NodeNotFound):
            self.tree.get_descendants('Gene1')

        with self.assertRaisesRegex(NodeNotFound, 'The node you provide Gene1 is not in the tree.'):
            self.tree.get_descendants('Gene1')


class TestGetAncestorsFunction(unittest.TestCase):
    tree = {}

    def setUp(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        with open(file_path, encoding="utf8") as f:
            jsonObj = yaml.load(f)
            self.objs = jsonObj.get('slots')
            self.tree = BioLinkSlotTree(self.objs)
            self.tree.construct()

    def test_multi_level_inheritency_is_correctly_passed(self):
        self.tree.construct()
        self.assertIn(self.tree.objects['related_to'], self.tree.get_ancestors('affects_abundance_of'))
        self.assertIn(self.tree.objects['affects'], self.tree.get_ancestors('affects_abundance_of'))
        self.assertNotIn(self.tree.objects['negatively_regulates'], self.tree.get_ancestors('affects_abundance_of'))

    def test_entity_without_ancestors_should_return_empty_array(self):
        self.assertEqual(len(self.tree.get_ancestors('related_to')), 0)
        self.assertEqual(len(self.tree.get_ancestors('regulates')), 0)

    def test_entity_not_in_the_tree_should_throw_an_error(self):
        with self.assertRaises(NodeNotFound):
            self.tree.get_ancestors('regulates1')

        with self.assertRaisesRegex(NodeNotFound, 'The node you provide regulates1 is not in the tree.'):
            self.tree.get_ancestors('regulates1')


class TestGetPathFunction(unittest.TestCase):
    tree = {}

    def setUp(self):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        with open(file_path, encoding="utf8") as f:
            jsonObj = yaml.load(f)
            self.objs = jsonObj.get('slots')
            self.tree = BioLinkSlotTree(self.objs)
            self.tree.construct()

    def test_return_all_intermediates_nodes_between_upstream_and_downstream_bigger_than_1(self):
        res = [item.name for item in self.tree.get_path('disrupts', 'related_to')]
        self.assertEqual(res, ['affects'])

    def test_return_the_intermediate_nodes_between_upstream_and_downstream_if_only_1(self):
        res = [item.name for item in self.tree.get_path('disrupts', 'related_to')]
        self.assertEqual(res, ['affects'])

    def test_return_empty_array_if_upstream_is_direct_parent_of_downstream(self):
        res = [item.name for item in self.tree.get_path('disrupts', 'affects')]
        self.assertEqual(res, [])

    def test_return_empty_array_if_downstream_has_no_parent(self):
        res = [item.name for item in self.tree.get_path('related_to', 'affects')]
        self.assertEqual(res, [])

    def test_downstream_node_not_in_the_tree_should_throw_an_error(self):
        with self.assertRaises(NodeNotFound):
            self.tree.get_path('affects1', 'affects2')

        with self.assertRaisesRegex(NodeNotFound, 'The node you provide affects1 is not in the tree.'):
            self.tree.get_path('affects1', 'affects2')

    def test_upstream_node_not_in_the_tree_should_throw_an_error(self):
        with self.assertRaises(NodeNotFound):
            self.tree.get_path('affects', 'affects2')

        with self.assertRaisesRegex(NodeNotFound, 'The node you provide affects2 is not in the tree.'):
            self.tree.get_path('affects', 'affects2')
