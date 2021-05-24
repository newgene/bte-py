import unittest
from biothings_explorer.biolink_model.index import BioLink
from biothings_explorer.biolink_model.tree.class_tree import BioLinkClassTree as BioLinkClassTree
from biothings_explorer.biolink_model.tree.slot_tree import BioLinkClassTree as BioLinkSlotTree


class TestBioLinkModule(unittest.TestCase):
    def test_load_function(self):
        biolink = BioLink()
        biolink.load()
        self.assertIn('classes', biolink.biolink_json)

    def test_load_sync_function(self):
        biolink = BioLink()
        biolink.load_sync()
        self.assertIn('classes', biolink.biolink_json)

    def test_class_tree_getter(self):
        biolink = BioLink()
        biolink.load()
        self.assertIsInstance(biolink.class_tree, BioLinkClassTree)
        self.assertIn('Gene', biolink.class_tree.objects)

    def test_class_tree_object_is_correctly_retrieved_in_sync_mode(self):
        biolink = BioLink()
        biolink.load_sync()
        self.assertIsInstance(biolink.class_tree, BioLinkClassTree)
        self.assertIn('Gene', biolink.class_tree.objects)

    def test_biolink_slot_tree_object_is_correctly_retrieved_in_async_mode(self):
        biolink = BioLink()
        biolink.load()
        self.assertIsInstance(biolink.slot_tree, BioLinkSlotTree)
        self.assertIn('related_to', biolink.slot_tree.objects)

    def test_biolink_slot_tree_object_is_correctly_retrieved_in_sync_mode(self):
        biolink = BioLink()
        biolink.load_sync()
        self.assertIsInstance(biolink.slot_tree, BioLinkSlotTree)
        self.assertIn('related_to', biolink.slot_tree.objects)
