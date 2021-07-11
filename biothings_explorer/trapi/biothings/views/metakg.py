import json
from tornado.web import RequestHandler
from biothings_explorer.trapi.utils.common import remove_quotes_from_query
from ..controllers.association import association


class RouteMetaKG2(RequestHandler):
    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        subject = kwargs.get('subject')
        _object = kwargs.get('object')
        predicate = kwargs.get('predicate')
        provided_by = kwargs.get('provided_by')
        api = kwargs.get('api')
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
        self.write({'associations': json.dumps(assocs)})
