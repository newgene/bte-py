from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from views.v0.views import Predicates, RouteQueryByAPI
from views.v1.views import (
    RouteMetaKG,
    RouteMetaKGByAPI,
    RouteMetaKGByTeam,
    RoutePredicates,
    RouteQueryTest,
    V1RouteQuery,
    RouteQueryV1ByAPI
)

define('port', default=8888, help='port to listen on')


def main():
    """Construct and serve the tornado application."""
    app = Application([
        ('/v0/predicates', Predicates),
        ('/v0/smartapi/([^/]+)/predicates', RouteQueryByAPI),
        ('/v1/meta_knowledge_graph', RouteMetaKG),
        ('/v1/smartapi/([^/]+D)/meta_knowledge_graph', RouteMetaKGByAPI),
        ('/v1/team/([^/]+D)/meta_knowledge_graph', RouteMetaKGByTeam),
        ('/v1/predicates', RoutePredicates),
        ('/v1/test/query', RouteQueryTest),
        ('/v1/query', V1RouteQuery),
        ('/v1/smartapi/([^/]+D)/query', RouteQueryV1ByAPI)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port, address='127.0.0.1')
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()
