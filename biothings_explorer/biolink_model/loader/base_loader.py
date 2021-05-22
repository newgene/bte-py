from abc import ABC
import yaml


class Loader(ABC):
    def yaml_2_json(self, _input):
        doc = yaml.load(_input)
        return doc

    def load(self, _input):
        pass
