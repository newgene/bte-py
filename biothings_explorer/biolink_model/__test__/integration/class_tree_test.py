import unittest
import os
import json
import yaml
from biothings_explorer.biolink_model.object.entity_object import Entity
from biothings_explorer.biolink_model.tree.class_tree import BioLinkClassTree


class TestConstructorFunction(unittest.TestCase):
    objs = {}
    tree = {}

    def setUp(self):
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        with open(file) as f:
            obj = yaml.load(f)
            self.objs = obj.get('classes')
            self.tree = BioLinkClassTree(self.objs)

    def test_constructor_function(self):
        self.tree.construct()
        self.assertIn('Gene', self.tree.objects)
        self.assertIsInstance(self.tree.objects['Gene'], Entity)
        self.assertIn('ChemicalSubstance', self.tree.objects)
        self.assertIn('OntologyClass', self.tree.objects)
        self.assertEqual(len(self.tree.objects.keys()), len(self.objs.keys()))

    def test_hierarchical_order_are_correctly_passed(self):
        self.tree.construct()
        self.assertIn('Gene', self.tree.objects['GenomicEntity'].children)
        self.assertIn('GenomicEntity', self.tree.objects['MolecularEntity'].children)
        self.assertNotIn('Gene', self.tree.objects['MolecularEntity'].children)
        self.assertEqual(len(self.tree.objects['Gene'].children), 0)


class TestGetDescendants(unittest.TestCase):
    tree = {}

    def setUp(self):
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        with open(file) as f:
            obj = yaml.load(f)
            self.objs = obj.get('classes')
            self.tree = BioLinkClassTree(self.objs)
            self.tree.construct()

    def test_multi_level_inheritency_correctly_passed(self):
        self.assertIn(self.tree.objects['Gene'], self.tree.get_descendants('MolecularEntity'))
        self.assertIsNotNone(self.tree.objects['NamedThing'])
        self.assertNotIn(self.tree.objects['NamedThing'], self.tree.get_descendants('MolecularEntity'))

    def test_entity_without_descendants_should_return_empty_array(self):
        self.assertEqual(len(self.tree.get_descendants('Gene')), 0)
        self.assertEqual(len(self.tree.get_descendants('ProteinIsoform')), 0)


class TestGetAncestors(unittest.TestCase):
    tree = {}

    def setUp(self):
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        with open(file) as f:
            obj = yaml.load(f)
            self.objs = obj.get('classes')
            self.tree = BioLinkClassTree(self.objs)
            self.tree.construct()

    def test_multi_level_inheritency_is_correctly_passed(self):
        self.tree.construct()
        self.assertIn(self.tree.objects['MolecularEntity'], self.tree.get_ancestors('Gene'))
        self.assertIn(self.tree.objects['NamedThing'], self.tree.get_ancestors('Gene'))
        self.assertNotIn(self.tree.objects['Protein'], self.tree.get_ancestors('Gene'))

    def test_entity_without_ancestors_should_return_empty_array(self):
        self.assertEqual(len(self.tree.get_ancestors('Entity')), 0)
        self.assertEqual(len(self.tree.get_ancestors('Annotation')), 0)


class TestGetPath(unittest.TestCase):
    tree = {}

    def setUp(self):
        file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'biolink.yaml'))
        with open(file) as f:
            obj = yaml.load(f)
            self.objs = obj.get('classes')
            self.tree = BioLinkClassTree(self.objs)
            self.tree.construct()

    def test_return_all_intermediates_nodes_between_upstream_and_downstream_if_bigger_than_1(self):
        res = [item.name for item in self.tree.get_path('Gene', 'NamedThing')]
        self.assertEqual(res, ["GenomicEntity", "MolecularEntity", "BiologicalEntity"])

    def test_return_all_intermediates_nodes_between_upstream_and_downstream_if_only_1(self):
        res = [item.name for item in self.tree.get_path('Gene', 'MolecularEntity')]
        self.assertEqual(res, ["GenomicEntity"])

    def test_return_empty_array_if_upstream_is_direct_parent_of_downstream(self):
        res = [item.name for item in self.tree.get_path('Gene', 'GenomicEntity')]
        self.assertEqual(res, [])

    def test_return_empty_array_if_downstream_has_no_parent(self):
        res = [item.name for item in self.tree.get_path('Entity', 'GenomicEntity')]
        self.assertEqual(res, [])
