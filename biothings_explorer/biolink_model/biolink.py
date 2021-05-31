from .loader.loader_factory import loader
from .loader.sync_loader_factory import sync_loader
from .tree.class_tree import BioLinkClassTree
from .tree.slot_tree import BioLinkClassTree as BiolinkSlotTree


class BioLink:
    _biolink_json = {}
    _biolink_class_tree = {}
    _biolink_slot_tree = {}

    def __init__(self):
        self._biolink_json = {}

    def load(self, source=None):
        l = loader(source)
        self._biolink_json = l.load(source)
        self._biolink_class_tree = BioLinkClassTree(self._biolink_json.get('classes'))
        self._biolink_slot_tree = BiolinkSlotTree(self._biolink_json.get('slots'))
        self._biolink_class_tree.construct()
        self._biolink_slot_tree.construct()

    def load_sync(self, source=None):
        l = sync_loader(source)
        self._biolink_json = l.load(source)
        self._biolink_class_tree = BioLinkClassTree(self._biolink_json.get('classes'))
        self._biolink_slot_tree = BiolinkSlotTree(self._biolink_json.get('slots'))
        self._biolink_class_tree.construct()
        self._biolink_slot_tree.construct()

    @property
    def class_tree(self):
        return self._biolink_class_tree

    @property
    def slot_tree(self):
        return self._biolink_slot_tree

    @property
    def biolink_json(self):
        return self._biolink_json
