from .base_loader import Loader


class FileLoader(Loader):
    def load(self, _input):
        return self.yaml_2_json(_input)
