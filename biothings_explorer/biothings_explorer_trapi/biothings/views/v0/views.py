from tornado.web import RequestHandler


class Predicates(RequestHandler):

    def get(self):
        """Handle a GET request for saying Hello World!."""
        self.write("Hello, world!")
