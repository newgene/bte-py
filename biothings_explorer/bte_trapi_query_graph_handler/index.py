from biothings_explorer.smartapi_kg.metakg import MetaKG
from .batch_edge_query import BatchEdgeQueryHandler
from .query_graph import QueryGraphHandler
from .graph.knowledge_graph import KnowledgeGraph
from .query_results import QueryResult
from .exceptions.invalid_query_graph_error import InvalidQueryGraphError
from .graph.graph import Graph
import os


class TRAPIQueryHandler:
    def __init__(self, options={}, smart_api_path=None, predicates_path=None, include_reasoner=True):
        self.logs = []
        self.options = options
        self.include_reasoner = include_reasoner
        self.resolve_output_ids = True if not ('enableIDResolution' in self.options and self.options['enableIDResolution']) else self.options['enableIDResolution']
        self.path = smart_api_path or os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'smartapi_specs.json'))
        self.predicate_path = predicates_path or os.path.abspath(os.path.join(os.path.dirname(__file__), 'predicates.json'))

    def _load_meta_kg(self):
        kg = MetaKG(self.path, self.predicate_path)
        kg.construct_MetaKG_sync(self.include_reasoner, self.options)
        return kg

    def get_response(self):
        self.bte_graph.notify()
        return {
            'message': {
                'query_graph': self.query_graph,
                'knowledge_graph': self.knowledge_graph.kg,
                'results': self.query_results.get_results()
            },
            'logs': self.logs
        }

    def set_query_graph(self, query_graph):
        self.query_graph = query_graph

    def _initialize_response(self):
        self.knowledge_graph = KnowledgeGraph()
        self.query_results = QueryResult()
        self.bte_graph = Graph()
        self.bte_graph.subscribe(self.knowledge_graph)

    def _process_query_graph(self, query_graph):
        try:
            query_graph_handler = QueryGraphHandler(query_graph)
            res = query_graph_handler.create_query_paths()
            self.logs = [*self.logs, *query_graph_handler.logs]
            return res
        except Exception as e:
            if isinstance(e, InvalidQueryGraphError):
                raise e
            else:
                raise InvalidQueryGraphError()

    def _create_batch_edge_query_handlers(self, query_paths, kg):
        handlers = {}
        for index in query_paths:
            handlers[index] = BatchEdgeQueryHandler(kg, self.resolve_output_ids)
            handlers[index].set_edges(query_paths[index])
            handlers[index].subscribe(self.query_results)
            handlers[index].subscribe(self.bte_graph)
        return handlers

    def query(self):
        self._initialize_response()
        smartapi_id = None
        if hasattr(self, 'smartapi_id'):
            smartapi_id = self.smartapi_id

        team = None
        if hasattr(self, 'team'):
            team = self.team

        kg = self._load_meta_kg()
        query_paths = self._process_query_graph(self.query_graph)
        handlers = self._create_batch_edge_query_handlers(query_paths, kg)
        # TODO 2nd item of handlers has incorrect output_equivalent_identifiers
        for handler in handlers.values():
            res = handler.query(handler.q_edges)
            self.logs = [*self.logs, *handler.logs]
            if len(res) == 0:
                return None
            else:
                handler.q_edges[0].output_equivalent_identifiers = res[0]['$edge_metadata']['trapi_qEdge_obj'].output_equivalent_identifiers
            handler.notify(res)
