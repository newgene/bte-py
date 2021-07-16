from tornado.testing import AsyncHTTPTestCase
from biothings_explorer.trapi.biothings import make_test_app


class TestPerformanceEndpoint(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def test_should_return_200_with_valid_response(self):
        response = self.fetch('/v1/performance')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers.get('Content-Type'), 'text/html')
