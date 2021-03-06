from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from dotenv import load_dotenv
from .views.v0.views import Predicates, RouteQueryByAPI
from .views.v1.views import (
    RouteMetaKG,
    RouteMetaKGByAPI,
    RouteMetaKGByTeam,
    RoutePredicates,
    RouteQueryTest,
    V1RouteQuery,
    RouteQueryV1ByAPI,
    RouteQueryV1ByTeam
)
from .views.metakg import RouteMetaKG2
from .views.performance import RoutePerformance
from .views.frontpage import RouteFrontPage

load_dotenv()
define('port', default=8888, help='port to listen on')


def make_app():
    app = Application([
        ('/', RouteFrontPage),
        ('/v0/predicates', Predicates),
        ('/v1/meta_knowledge_graph', RouteMetaKG),
        (r"/v1/smartapi/([^/]*)/meta_knowledge_graph", RouteMetaKGByAPI),
        (r"/v1/smartapi/([^/]*)/query", RouteQueryV1ByAPI),
        (r"/v0/smartapi/([^/]*)/predicates", RouteQueryByAPI),
        (r"/v1/team/([^/]*)/meta_knowledge_graph", RouteMetaKGByTeam),
        ('/v1/predicates', RoutePredicates),
        ('/v1/test/query', RouteQueryTest),
        ('/v1/query', V1RouteQuery),
        (r"/v1/team/([^/]*)/query", RouteQueryV1ByTeam),
        (r"/metakg", RouteMetaKG2),
        ('/v1/performance', RoutePerformance),
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port, address='127.0.0.1')
    return http_server


def main():
    """Construct and serve the tornado application."""
    make_app()
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()


def make_test_app():
    return make_app()
