from abc import ABC
from .base_object import BaseObject
from ..utils import underscore, pascal_case


class Slot(BaseObject, ABC):
    _domain = ''
    _range = ''
    _inverse = ''
    _exact_mapping = []
    _close_mapping = []
    _narrow_mapping = []
    _symmetric = False

    def __init__(self, name, info):
        super(Slot, self).__init__(name, info)
        self._parent = info.get('is_a') if not info.get('is_a') else underscore(info.get('is_a'))
        self._inverse = info.get('inverse') if not info.get('inverse') else underscore(info.get('inverse'))
        self._domain = info.get('domain') if not info.get('domain') else pascal_case(info.get('domain'))
        self._range = info.get('range') if not info.get('range') else pascal_case(info.get('range'))
        self._symmetric = False if not info.get('symmetric') else True
        self._exact_mapping = info.get('exact_mapping')
        self._close_mapping = info.get('close_mapping')
        self._narrow_mapping = info.get('narrow_mapping')

    @property
    def inverse(self):
        return self._inverse

    @inverse.setter
    def inverse(self, value):
        self._inverse = value

    @property
    def symmetric(self):
        return self._symmetric

    @property
    def domain(self):
        return self._domain

    @property
    def range(self):
        return self._range

    @property
    def exact_mapping(self):
        return self._exact_mapping

    @property
    def narrow_mapping(self):
        return self._narrow_mapping

    @property
    def close_mapping(self):
        return self._close_mapping

    def add_child(self, child):
        self._children.append(underscore(child))
