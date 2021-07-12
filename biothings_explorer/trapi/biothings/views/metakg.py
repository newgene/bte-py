import json
from tornado.web import RequestHandler, MissingArgumentError
from biothings_explorer.trapi.utils.common import remove_quotes_from_query
from ..controllers.association import association


class RouteMetaKG2(RequestHandler):
    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        try:
            subject = self.get_argument('subject')
        except MissingArgumentError:
            subject = None
        try:
            _object = self.get_argument('object')
        except MissingArgumentError:
            _object = None
        try:
            provided_by = self.get_argument('provided_by')
        except MissingArgumentError:
            provided_by = None
        try:
            predicate = self.get_argument('predicate')
        except MissingArgumentError:
            predicate = None
        try:
            api = self.get_argument('api')
        except MissingArgumentError:
            api = None

        if api:
            api = remove_quotes_from_query(api)
        if provided_by:
            provided_by = remove_quotes_from_query(provided_by)
        assocs = association(subject,
                             _object,
                             predicate,
                             api,
                             provided_by
                             )
        self.write({'associations': assocs})
