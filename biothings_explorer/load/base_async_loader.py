import requests
from .base_loader import BaseLoader


class BaseAsyncLoader(BaseLoader):
    _url = ''

    def __init__(self, url):
        super(BaseAsyncLoader, self).__init__()
        self._url = url

    def fetch(self):
        try:
            response = requests.get(self._url)
            return response
        except Exception as e:
            pass

    def parse(self):
        return []

    def load(self):
        specs = self.fetch()
        return self.parse(specs)
