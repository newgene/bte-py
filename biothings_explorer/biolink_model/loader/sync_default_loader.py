import os
from .base_loader import Loader


class SyncDefaultLoader(Loader):
    def load(self, _input=None):
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, 'data', 'biolink.yaml'))
        return self.yaml_2_json(file_path)
