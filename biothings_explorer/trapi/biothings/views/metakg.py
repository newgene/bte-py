import json
from tornado.web import RequestHandler
from biothings_explorer.trapi.utils.common import remove_quotes_from_query
from ..controllers.association import association


class RouteMetaKG2(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        data = json.loads(self.request.body)
        api = data['message'].get('api')
        provided_by = data['message'].get('provided_by')
        if api:
            api = remove_quotes_from_query(api)
        if provided_by:
            provided_by = remove_quotes_from_query(provided_by)
        assocs = association(data['message'].get('subject'),
                             data['message'].get('object'),
                             data['message'].get('predicate'),
                             api,
                             provided_by
                             )
        self.write(json.dumps(assocs))
