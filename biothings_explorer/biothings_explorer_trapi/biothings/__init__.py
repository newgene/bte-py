from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from views.v0.views import Predicates

define('port', default=8888, help='port to listen on')


def main():
    """Construct and serve the tornado application."""
    app = Application([
        ('/v0/predicates', Predicates)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    print('Listening on http://localhost:%i' % options.port)
    IOLoop.current().start()
