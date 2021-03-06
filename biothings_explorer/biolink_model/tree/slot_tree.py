from abc import ABC
from biothings_explorer.biolink_model.object.slot_object import Slot
from ..utils import underscore
from .base_tree import BaseTree


class BioLinkClassTree(BaseTree, ABC):
    _objects_in_yaml = {}
    _objects_in_tree = {}

    def __init__(self, objects):
        super(BioLinkClassTree, self).__init__(objects)
        self._modify = underscore

    def construct(self):
        super(BioLinkClassTree, self).construct()
        for name in self._objects_in_tree:
            self.infer_inverse_relationship(name)

    @property
    def objects(self):
        return self._objects_in_tree

    def add_new_object_to_tree(self, name):
        self._objects_in_tree[self._modify(name)] = Slot(self._modify(name), self._objects_in_yaml.get(name))

    def get_descendants(self, name):
        return super(BioLinkClassTree, self).get_descendants(name)

    def get_ancestors(self, name):
        return super(BioLinkClassTree, self).get_ancestors(name)

    def get_path(self, downstream_node, upstream_node):
        return super(BioLinkClassTree, self).get_path(downstream_node, upstream_node)

    def infer_inverse_relationship(self, name):
        if not self._objects_in_tree[self._modify(name)].inverse:
            inverse = None
            for key, obj in self._objects_in_tree.items():
                if obj.inverse == self._modify(name):
                    inverse = obj
            if inverse:
                self._objects_in_tree[self._modify(name)].inverse = inverse.name
