from abc import ABC
import yaml


class Loader(ABC):
    def yaml_2_json(self, _input):
        try:
            with open(_input) as f:
                doc = yaml.load(f)
                return doc
        except Exception as e:
            doc = yaml.load(_input)
            #print(e)
            return doc

    def load(self, _input):
        pass
