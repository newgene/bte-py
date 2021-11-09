from biothings_explorer.smartapi_kg.metakg import MetaKG
from .batch_edge_query import BatchEdgeQueryHandler
from .query_graph import QueryGraphHandler
from .graph.knowledge_graph import KnowledgeGraph
from .query_results import QueryResult
from .exceptions.invalid_query_graph_error import InvalidQueryGraphError
from .graph.graph import Graph
from .edge_manager import EdgeManager
import os


class TRAPIQueryHandler:
    def __init__(self, options={}, smart_api_path=None, predicates_path=None, include_reasoner=True):
        self.logs = []
        self.options = options
        self.include_reasoner = include_reasoner
        self.resolve_output_ids = True if self.options.get('enableIDResolution') is None else self.options['enableIDResolution']
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

    def _create_batch_edge_query_handlers_for_current(self, current_edge, kg):
        handler = BatchEdgeQueryHandler(kg, self.resolve_output_ids)
        handler.set_edges(current_edge)
        handler.subscribe(self.query_results)
        handler.subscribe(self.bte_graph)
        return handler

    def query(self):
        self._initialize_response()
        kg = self._load_meta_kg()
        query_paths = self._process_query_graph(self.query_graph)
        handlers = self._create_batch_edge_query_handlers_for_current(query_paths, kg)
        for handler in handlers.values():
            res = handler.query(handler.q_edges)
            self.logs = [*self.logs, *handler.logs]
            if len(res) == 0:
                return None
            else:
                handler.q_edges[0].output_equivalent_identifiers = res[0]['$edge_metadata']['trapi_qEdge_obj'].output_equivalent_identifiers
            handler.notify(res)

    def query_2(self):
        self._initialize_response()
        kg = self._load_meta_kg(self.smartapi_id, self.team)
        query_edges = self._process_query_graph(self.query_graph)
        manager = EdgeManager(query_edges)
        while manager.get_edges_not_executed():
            current_edge = manager.get_next()
            # if current_edge['requires_intersection']:
            #     current_edge.choose_lower_entity_value()
            handler = self._create_batch_edge_query_handlers_for_current(current_edge, kg)
            res = handler.query_2(handler.q_edges)
            self.logs = [*self.logs, *handler.logs]
            if len(res) == 0:
                return
            current_edge.store_results(res)
            manager.update_edges_entity_counts(res, current_edge)
            current_edge['executed'] = True
        manager.gather_results()
        self.logs = [*self.logs, *manager.logs]
        mock_handler = self._create_batch_edge_query_handlers_for_current([], kg)
        mock_handler.notify(manager.results)
