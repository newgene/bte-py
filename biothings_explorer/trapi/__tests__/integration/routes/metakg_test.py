from tornado.testing import AsyncHTTPTestCase
from biothings_explorer.trapi.biothings import make_test_app


class TestMetaKGEndpoint(AsyncHTTPTestCase):
    def get_app(self):
        return make_test_app()

    def get_url(self, path):
        """Returns an absolute url for the given path on the test server."""
        return '%s://localhost:%s%s' % (self.get_protocol(),
                                        self.get_http_port(), path)

    def test_should_return_200_with_valid_response_using_default_values(self):
        response = self.fetch('/v1/metakg')
        self.assertEqual(response.code, 200)
