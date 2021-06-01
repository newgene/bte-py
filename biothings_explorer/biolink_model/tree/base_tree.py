from abc import ABC
from ..exceptions.node_not_found import NodeNotFound


class BaseTree(ABC):
    _objects_in_tree = {}
    _objects_in_yaml = {}
    _modify = None

    def __init__(self, objects=None):
        self._objects_in_yaml = objects
        self._objects_in_tree = {}
        self._modify = lambda _input: _input


    @property
    def objects(self):
        return self._objects_in_tree

    def get_unique_objects(self, objects):
        tmp_objs = {}
        for obj in objects:
            tmp_objs[obj.name] = obj
        return tmp_objs.values()

    def check_if_node_in_tree(self, name):
        if self._modify(name) not in self._objects_in_tree:
            raise NodeNotFound(f'The node you provide {self._modify(name)} is not in the tree.')

    def add_new_object_to_tree(self, name):
        pass

    def construct(self):
        self._objects_in_tree = {}
        for name in self._objects_in_yaml:
            self.add_new_object_to_tree(name)
        for name in self._objects_in_yaml:
            if 'is_a' in self._objects_in_yaml[name]:
                try:
                    self._objects_in_tree.get(self._modify(self._objects_in_yaml.get(name, {})['is_a'])).add_child(name)
                except Exception as e:
                    print(e)
                    pass

    def get_descendants(self, name):
        self.check_if_node_in_tree(name)
        descendants = []
        for child in self._objects_in_tree[self._modify(name)].children:
            descendants.append(self._objects_in_tree[child])
            descendants = [*descendants, *self.get_descendants(child)]
        return self.get_unique_objects(descendants)

    def get_ancestors(self, name):
        self.check_if_node_in_tree(name)
        ancestors = []
        if not self._objects_in_tree[self._modify(name)].parent:
            return ancestors

        ancestors.append(self._objects_in_tree[self._objects_in_tree[self._modify(name)].parent])
        ancestors = [*ancestors, *self.get_ancestors(self._objects_in_tree[self._modify(name)].parent)]
        return self.get_unique_objects(ancestors)

    def get_path(self, downstream_node, upstream_node):
        self.check_if_node_in_tree(downstream_node)
        self.check_if_node_in_tree(upstream_node)
        path = []
        if not self._objects_in_tree[self._modify(downstream_node)].parent or \
                self._objects_in_tree[self._modify(downstream_node)].parent == self._modify(upstream_node):
            return path
        path.append(self._objects_in_tree[self._objects_in_tree[self._modify(downstream_node)].parent])
        path = [*path, *self.get_path(self._objects_in_tree[self._modify(downstream_node)].parent, upstream_node)]
        return self.get_unique_objects(path)
