import os
from os.path import abspath
from .operations_builder.async_builder_factory import async_builder_factory
from .operations_builder.sync_builder_factory import sync_builder_factory
from .filter import ft


class MetaKG:
    _ops = []
    _file_path = ''
    _predicates_path = ''

    def __init__(self, path=None, predicates_path=None):
        self._ops = []
        self.path = path
        self.predicates_path = predicates_path

    @property
    def predicates_path(self):
        return self._predicates_path

    @property
    def path(self):
        return self._file_path

    @path.setter
    def path(self, file_path):
        if not file_path:
            directory = os.path.dirname(__file__)
            #os.path.dirname(os.path.abspath('biothings_explorer/smartapi_kg/data/smartapi_specs.json'))
            self._file_path = os.path.join(directory, 'data', 'smartapi_specs.json')
        else:
            self._file_path = file_path

    @predicates_path.setter
    def predicates_path(self, file_path):
        if not file_path:
            directory = os.path.dirname(__file__)
            #self._predicates_path = abspath('./biothings_explorer/smartapi_kg/data/predicates.json')
            self._predicates_path = os.path.join(directory, 'data', 'predicates.json')
        else:
            self._predicates_path = file_path

    @property
    def ops(self):
        return self._ops

    def construct_MetaKG(self, include_reasoner=False, options={}):
        self._ops = async_builder_factory(options, include_reasoner)
        return self._ops

    def construct_MetaKG_sync(self, include_reasoner=False, options={}):
        self._ops = sync_builder_factory(
            options,
            include_reasoner,
            self._file_path,
            self._predicates_path
        )
        return self._ops

    def filter(self, criteria):
        return ft(self.ops, criteria)
