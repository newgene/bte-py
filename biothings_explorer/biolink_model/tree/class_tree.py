from abc import ABC
from ..object.entity_object import Entity
from ..utils import pascal_case
from .base_tree import BaseTree


class BioLinkClassTree(BaseTree, ABC):
    _objects_in_yaml = {}
    _objects_in_tree = {}
    
    def __init__(self, objects):
        super(BioLinkClassTree, self).__init__(objects)
        self._modify = pascal_case
    
    @property
    def objects(self):
        return self._objects_in_tree
    
    def add_new_object_to_tree(self, name):
        self._objects_in_tree[self._modify(name)] = Entity(self._modify(name), self._objects_in_yaml[name])
        
    def get_descendants(self, name):
        return super(BioLinkClassTree, self).get_descendants(name)
    
    def get_ancestors(self, name):
        return super(BioLinkClassTree, self).get_ancestors(name)
    
    def get_path(self, downstream_node, upstream_node):
        return super(BioLinkClassTree, self).get_path(downstream_node, upstream_node)
