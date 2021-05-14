from .base_operations_builder import BaseOperationsBuilder
from ..load.sync_loader_factory import sync_loader_factory


class SyncOperationsBuilder(BaseOperationsBuilder):
    _file_path = ''

    def __init__(self, options, path):
        super(SyncOperationsBuilder, self).__init__(options)
        self._file_path = path

    def build(self):
        specs = sync_loader_factory(
            self._options.smart_API_id,
            self._options.team_name,
            self._options.tag,
            self._options.component,
            self._options.api_names,
            self._file_path,
        )

        return self.load_ops_from_specs(specs)
