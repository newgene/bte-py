from abc import ABC


class BaseObject(ABC):
    _description = ''
    _parent = ''
    _children = []
    _name = ''

    def __init__(self, name, info):
        self._name = name
        self._description = info.get('description')
        self._parent = info.get('is_a')
        self._children = []

    @property
    def get_parent(self):
        return self._parent

    @property
    def description(self):
        return self._description

    @property
    def name(self):
        return self._name

    def add_child(self, child):
        pass
