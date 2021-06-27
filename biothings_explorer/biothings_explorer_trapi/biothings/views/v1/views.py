from tornado.web import RequestHandler
import json
from biothings_explorer.biothings_explorer_trapi.biothings.controllers.meta_knowledge_graph import MetaKnowledgeGraphHandler
from biothings_explorer.biothings_explorer_trapi.biothings.controllers.predicates import PredicatesHandler


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