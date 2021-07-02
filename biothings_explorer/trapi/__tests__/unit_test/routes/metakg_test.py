import unittest
import requests
from biothings_explorer.trapi.biothings.controllers.association import association


class TestPerformanceEndpoint(unittest.TestCase):
    response = requests.get('http://jsonplaceholder.typicode.com/todos')

