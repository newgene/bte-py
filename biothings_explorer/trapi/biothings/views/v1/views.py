from tornado.web import RequestHandler
import json
import os
from biothings_explorer.trapi.biothings.controllers.meta_knowledge_graph import MetaKnowledgeGraphHandler
from biothings_explorer.trapi.biothings.controllers.predicates import PredicatesHandler
from biothings_explorer.query_graph_handler.index import TRAPIQueryHandler
from .config import API_LIST
from biothings_explorer.trapi.utils.common import remove_quotes_from_query
from biothings_explorer.trapi.biothings.controllers.association import association
import json


class RouteMetaKG(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        meta_kg_handler = MetaKnowledgeGraphHandler(None)
        kg = meta_kg_handler.get_kg()
        self.write(json.dumps(kg))


class RouteMetaKGByAPI(RequestHandler):
    def get(self, slug):
        self.set_header('Content-Type', 'application/json')
        meta_kg_handler = MetaKnowledgeGraphHandler(slug)
        kg = meta_kg_handler.get_kg()
        self.write(json.dumps(kg))


class RouteMetaKGByTeam(RequestHandler):
    def get(self, slug):
        self.set_header('Content-Type', 'application/json')
        meta_kg_handler = MetaKnowledgeGraphHandler(None, slug)
        kg = meta_kg_handler.get_kg()
        self.write(json.dumps(kg))


class RoutePredicates(RequestHandler):
    def get(self):
        self.set_header('Content-Type', 'application/json')
        predicate_handler = PredicatesHandler(None)
        predicates = predicate_handler.get_predicates()
        self.write(json.dumps(predicates))


class RouteQueryTest(RequestHandler):
    def post(self):
        self.set_header('Content-Type', 'application/json')
        data = json.loads(self.request.body)
        query_graph = data['message']['query_graph']
        smartapi = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'test', 'smartapi.json'))
        handler = TRAPIQueryHandler({}, smartapi, None, False)
        handler.set_query_graph(query_graph)
        handler.query()
        # vanilla json dumps throws error when encountering datetime
        # the below json dumps can also handle datetime errors
        self.write(json.dumps(handler.get_response(), indent=4, sort_keys=True, default=str))


class V1RouteQuery(RouteQueryTest):
    def post(self):
        try:
            self.set_header('Content-Type', 'application/json')
            data = json.loads(self.request.body)
            query_graph = data['message']['query_graph']
            smartapi_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'test', 'smartapi.json'))
            handler = TRAPIQueryHandler({'api_names': API_LIST}, smartapi_path)
            handler.set_query_graph(query_graph)
            handler.query()
            self.write(json.dumps(handler.get_response(), indent=4, sort_keys=True, default=str))
        except Exception as e:
            print(e)
            self.set_status(400)
            self.write({'error': 'Your input query graph is invalid'})


class RouteQueryV1ByAPI(RequestHandler):
    def post(self, slug):
        try:

            self.set_header('Content-Type', 'application/json')
            data = json.loads(self.request.body)
            query_graph = data['message']['query_graph']
            enableIDResolution = False if slug in ['5be0f321a829792e934545998b9c6afe',
                                                   '978fe380a147a8641caf72320862697b'] else True
            smartapi_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'test', 'smartapi.json'))

            handler = TRAPIQueryHandler(
                {
                    'smartAPIID': slug,
                    'enableIDResolution': enableIDResolution,
                },
                smartapi_path,
                None,
                False
            )
            handler.set_query_graph(query_graph)
            handler.query()
            self.write(json.dumps(handler.get_response(), indent=4, sort_keys=True, default=str))
        except Exception as e:
            print(e)
            self.set_status(400)
            self.write({'error': 'Your input query graph is invalid'})


class RouteQueryV1ByTeam(RequestHandler):
    def post(self, slug):
        try:
            self.set_header('Content-Type', 'application/json')
            data = json.loads(self.request.body)
            query_graph = data['message']['query_graph']
            enableIDResolution = False if slug == 'Text Mining Provider' else True
            smartapi_path = os.path.abspath(
                os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, 'test', 'smartapi.json'))
            handler = TRAPIQueryHandler(
                {
                    'teamName': slug,
                    'enableIDResolution': enableIDResolution
                },
                smartapi_path,
                None,
                False
            )
            handler.set_query_graph(query_graph)
            handler.query()
            self.write(json.dumps(handler.get_response(), indent=4, sort_keys=True, default=str))
        except Exception as e:
            print(e)
            self.set_status(400)
            self.write({'error': 'Your input query graph is invalid'})
