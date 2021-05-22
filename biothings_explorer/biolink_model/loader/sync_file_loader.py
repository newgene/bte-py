from .base_loader import Loader


class SyncFileLoader(Loader):
    def load(self, _input):
        with open(_input) as f:
            return self.yaml_2_json(_input)
