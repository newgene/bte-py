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
        self.assertEqual(self.tree.objects.keys(), self.objs.keys())

    def test_hierarchical_order_are_correctly_passed(self):
        self.tree.construct()
        self.assertIn('Gene', self.tree.objects['GenomicEntity'].children)
        self.assertIn('GenomicEntity', self.tree.objects['MolecularEntity'].children)
        self.assertNotIn('Gene', self.tree.objects['MolecularEntity'].children)
        self.assertEqual(len(self.tree.objects['Gene'].children), 0)
