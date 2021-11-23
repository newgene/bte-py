import copy
from biothings_explorer.smartapi_kg.metakg import MetaKG
from .batch_edge_query import BatchEdgeQueryHandler
from .query_graph import QueryGraphHandler
from .graph.knowledge_graph import KnowledgeGraph
from .query_results import QueryResult
from .exceptions.invalid_query_graph_error import InvalidQueryGraphError
from .graph.graph import Graph
from .edge_manager import EdgeManager
from .qedge2bteedge import QEdge2BTEEdgeHandler
from .log_entry import LogEntry
import json
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
            'workflow': [
                {'id': 'lookup'}
            ],
            'message': {
                'query_graph': self.query_graph,
                'knowledge_graph': self.knowledge_graph.kg,
                'results': self.query_results.get_results()
            },
            'logs': self.logs
        }

    def set_query_graph(self, query_graph):
        for node_id in query_graph['nodes']:
            if query_graph['nodes'].get(node_id):
                current_node = query_graph['nodes'][node_id]
                if current_node.get('categories'):
                    if 'biolink:Protein' in current_node['categories'] and 'biolink:Gene' not in current_node['categories']:
                        current_node['categories'].append('biolink:Gene')
        self.query_graph = query_graph

    def _initialize_response(self):
        self.knowledge_graph = KnowledgeGraph()
        self.query_results = QueryResult()
        self.bte_graph = Graph()
        self.bte_graph.subscribe(self.knowledge_graph)

    def _process_query_graph(self, query_graph):
        try:
            query_graph_handler = QueryGraphHandler(query_graph)
            res = query_graph_handler.calculate_edges()
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
            handlers[index] = BatchEdgeQueryHandler(kg, self.resolve_output_ids, {'caching': self.options['caching']})
            handlers[index].set_edges(query_paths[index])
            handlers[index].subscribe(self.query_results)
            handlers[index].subscribe(self.bte_graph)
        return handlers

    def _create_batch_edge_query_handlers_for_current(self, current_edge, kg):
        handler = BatchEdgeQueryHandler(kg, self.resolve_output_ids, {'caching': self.options['caching']})
        handler.set_edges(current_edge)
        # handler.subscribe(self.query_results)
        # handler.subscribe(self.bte_graph)
        return handler

    def _edges_supported(self, q_edges, kg):
        q_edges = copy.deepcopy(q_edges)
        manager = EdgeManager(q_edges)
        edges_missing_ops = {}
        while manager.get_edges_not_executed():
            current_edge = manager.get_next()
            edge_converter = QEdge2BTEEdgeHandler([current_edge], kg)
            s_api_edges = edge_converter.get_smart_api_edges(current_edge)
            if not len(s_api_edges):
                edges_missing_ops[current_edge['q_edge']['id']] = current_edge['reverse']
            current_edge['executed'] = True
            current_edge['object']['entity_count'] = 1
            current_edge['subject']['entity_count'] = 1
        length = len(edges_missing_ops.keys())
        edges_to_log = [f"(reversed {edge})" if _reversed else f"({edge})" for edge, _reversed in edges_missing_ops.items()]
        if len(edges_to_log) > 1:
            edges_to_log = f"[{','.join(edges_to_log)}]"
        else:
            edges_to_log = f"{','.join(edges_to_log)}"
        if length > 0:
            terminate_log = f"Query Edges{'s' if length > 1 else ''} {edges_to_log} {'have' if length > 1 else 'has'}" \
                            f" no SmartAPI edges. Your query terminates."
            self.logs.append(LogEntry('WARNING', None, terminate_log))
            return False
        else:
            return True

    def query(self):
        self._initialize_response()
        kg = self._load_meta_kg(self.smartapi_id, self.team)
        query_edges = self._process_query_graph(self.query_graph)
        if not self._edges_supported(query_edges, kg):
            return
        manager = EdgeManager(query_edges)
        while manager.get_edges_not_executed():
            current_edge = manager.get_next()
            handler = self._create_batch_edge_query_handlers_for_current(current_edge, kg)
            res = handler.query(handler.q_edges)
            self.logs = [*self.logs, *handler.logs]
            if len(res) == 0:
                return
            current_edge.store_results(res)
            manager.update_edge_results(current_edge)
            manager.update_all_other_edges(current_edge)
            current_edge['executed'] = True
        manager.collect_results()
        self.logs = [*self.logs, *manager.logs]
        self.bte_graph.update(manager.get_results())
        self.query_results.update(manager.get_organized_results())