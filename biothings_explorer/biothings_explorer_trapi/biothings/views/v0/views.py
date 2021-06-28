from tornado.web import RequestHandler
from biothings_explorer.biothings_explorer_trapi.biothings.controllers.predicates import PredicatesHandler
import json


class Predicates(RequestHandler):
    def get(self):
        """Handle a GET request for saying Hello World!."""
        self.set_header('Content-Type', 'application/json')
        try:
            predicate_handler = PredicatesHandler(None, "0.9.2")
            predicates = predicate_handler.get_predicates()
            data = json.dumps(predicates)
            self.write(data)
        except Exception as e:
            self.write({'error': 'An unexpected error occurred'})


class RouteQueryByAPI(RequestHandler):
    def get(self, smartapiID):
        self.set_header('Content-Type', 'application/json')
        try:
            handler = PredicatesHandler(smartapiID, '0.9.2')
            predicates = handler.get_predicates()
            self.write(json.dumps(predicates))
        except Exception as e:
            pass
