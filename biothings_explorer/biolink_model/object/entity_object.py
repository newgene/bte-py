from abc import ABC
from .base_object import BaseObject
from ..utils import pascal_case


class Entity(BaseObject, ABC):
    _id_prefixes = []

    def __init__(self, name, info):
        super(Entity, self).__init__(name, info)
        self.id_prefixes = info.get('id_prefixes')
        self._parent = info.get('is_a') if not info.get('is_a') else pascal_case(info.get('is_a'))

    @property
    def id_prefixes(self):
        return self._id_prefixes

    @id_prefixes.setter
    def id_prefixes(self, id_prefixes):
        if self._name == 'Gene':
            self._id_prefixes = ['SYMBOL', 'OMIM', 'UMLS', *id_prefixes]
        elif self._name == 'ChemicalSubstance':
            self._id_prefixes = ['UMLS'] if not id_prefixes else ['UMLS', *id_prefixes]
        elif self._name == 'SmallMolecule':
            self._id_prefixes = ['UMLS', *id_prefixes]
        elif self._name == 'Disease':
            self._id_prefixes = ['GARD', *id_prefixes]
        else:
            self._id_prefixes = id_prefixes

    def add_child(self, child):
        self._children.append(pascal_case(child))
