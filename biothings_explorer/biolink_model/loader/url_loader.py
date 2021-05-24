import requests
from .base_loader import Loader


class URLLoader(Loader):
    def load(self, _input):
        res = requests.get(_input)
        data = res.text
        return self.yaml_2_json(data)
