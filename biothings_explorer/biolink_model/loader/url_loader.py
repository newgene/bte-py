import requests
from .base_loader import Loader


class URLLoader(Loader):
    def load(self, _input):
        try:
            res = requests.get(_input)
            if res.status_code != 200:
                raise Exception(f'Failed to load BioLink Model. Query to ${_input} returns ${res.status_code} status code.')
            data = res.text
            return self.yaml_2_json(data)
        except requests.exceptions.RequestException as err:
            raise Exception(f'Failed to load BioLink Model. Query to {_input} raise an exception.')

