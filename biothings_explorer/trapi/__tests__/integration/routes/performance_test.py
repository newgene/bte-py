from tornado.testing import AsyncHTTPTestCase
from biothings_explorer.trapi.biothings import make_test_app


class TestPerformanceEndpoint(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def get_url(self, path):
        """Returns an absolute url for the given path on the test server."""
        return '%s://localhost:%s%s' % (self.get_protocol(),
                                        self.get_http_port(), path)

    def test_should_return_200_with_valid_response(self):
        response = self.fetch('/v1/performance')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers.get('Content-Type'), 'text/html')
