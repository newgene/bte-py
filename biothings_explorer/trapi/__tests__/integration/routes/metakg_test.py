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

    def test_should_return_200_with_valid_response_when_user_specify_api(self):
        response = self.fetch('/metakg?api=MyGene.info%20API')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('associations', data)
        apis = list(set(item['api']['name'] for item in data['associations']))
        self.assertEqual(['MyGene.info API'], apis)

    def test_should_return_200_with_valid_response_when_user_specify_provided_by(self):
        response = self.fetch('/metakg?provided_by=drugbank')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('associations', data)
        res = list(set(item['provided_by'] for item in data['associations']))
        self.assertEqual(res, ['drugbank'])

    def test_should_return_200_with_valid_response_when_user_specify_subject(self):
        response = self.fetch('/metakg?subject=Gene')
        self.assertEqual(response.code, 200)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('associations', data)
        res = list(set(item['subject'] for item in data['associations']))
        self.assertEqual(['Gene'], res)
