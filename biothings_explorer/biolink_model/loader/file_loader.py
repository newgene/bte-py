from .base_loader import Loader


class FileLoader(Loader):
    def load(self, _input):
        with open(_input) as f:
            return self.yaml_2_json(f)
