import json
from tornado.web import RequestHandler
from biothings_explorer.trapi.utils.common import remove_quotes_from_query
from ..controllers.association import association


class RouteMetaKG(RequestHandler):
    def get(self, **kwargs):
        self.set_header('Content-Type', 'application/json')
        api = kwargs.get('api', None)
        source = kwargs.get('provided_by', None)
        assocs = association(kwargs.get('subject'), kwargs.get('object'), kwargs.get('predicate'), api, source)
        self.write({'association': json.dumps(assocs)})
