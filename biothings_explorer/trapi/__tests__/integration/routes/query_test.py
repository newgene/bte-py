from tornado.testing import AsyncHTTPTestCase
from biothings_explorer.trapi.biothings import make_test_app
import json


class TestQueryEndpoint(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def test_input_query_graph_that_doesnt_pass_swagger_validation_should_return_400_error(self):
        invalid_input_query_graph = {
            'message': 1
        }
        response = self.fetch('/v1/query', method="POST", body=json.dumps(invalid_input_query_graph))
        self.assertEqual(response.code, 400)
        data = json.loads(response.body.decode('utf-8'))
        self.assertIn('application/json', response.headers['Content-Type'])
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Your input query graph is invalid')
