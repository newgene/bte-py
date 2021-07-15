import unittest
from tornado.testing import AsyncHTTPTestCase, gen_test
from unittest.mock import Mock, MagicMock
import requests
from biothings_explorer.trapi.biothings.controllers.association import association
from biothings_explorer.trapi.biothings import make_test_app


class TestPerformanceEndpoint(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def test_should_return_404_when_loading_metakg_failed(self):
        mock = Mock(side_effect=Exception('Boom!'))
        association = mock
        response = self.fetch('/metakg')
        print(response)
