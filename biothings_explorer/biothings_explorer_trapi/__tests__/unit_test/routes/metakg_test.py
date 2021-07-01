import unittest
import requests
from biothings_explorer.biothings_explorer_trapi.biothings.controllers.association import association


class TestPerformanceEndpoint(unittest.TestCase):
    response = requests.get('http://jsonplaceholder.typicode.com/todos')

