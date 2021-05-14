from abc import ABC, abstractmethod
from biothings_explorer.smartapi_kg.parser.index import API


class BaseOperationsBuilder(ABC):
    _options = {}

    def __init__(self, options):
        self._options = options

    def load_ops_from_specs(self, specs):
        all_ops = []
        for spec in specs:
            try:
                parser = API(spec)
                ops = parser.metadata['operations']
                all_ops = [*all_ops, *ops]
            except Exception as e:
                pass
        return all_ops

    @abstractmethod
    def build(self):
        pass
