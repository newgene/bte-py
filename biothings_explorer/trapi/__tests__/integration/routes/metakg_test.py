from tornado.testing import AsyncHTTPTestCase
from biothings_explorer.trapi.biothings import make_test_app
import json


class TestMetaKGEndpoint(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def test_should_return_200_with_valid_response_using_default_values(self):
        response = self.fetch('/metakg')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('associations', data)
        self.assertGreater(len(data['associations']), 100)
