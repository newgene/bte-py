from biothings_explorer.call_apis.query import APIQueryDispatcher
from .qedge2bteedge import QEdge2BTEEdgeHandler
from .update_nodes import NodesUpdateHandler
from .cache_handler import CacheHandler
from .utils import to_array, remove_biolink_prefix


class BatchEdgeQueryHandler:
    def __init__(self, kg, resolve_output_ids=True, options=None):
        self.kg = kg
        self.subscribers = []
        self.logs = []
        self.resolve_output_ids = resolve_output_ids
        self.caching = options and options['caching']

    def set_edges(self, q_edges):
        self.q_edges = q_edges

    def get_edges(self):
        return self.q_edges

    def _expand_bte_edges(self, bte_edges):
        return bte_edges

    def _query_bte_edges(self, bte_edges):
        executor = APIQueryDispatcher(bte_edges)
        res = executor.query(self.resolve_output_ids)
        self.logs = [*self.logs, *executor.logs]
        return res

    def _post_query_filter(self, response):
        response = [res for res in response if res]
        return response

    def _rm_equivalent_duplicates(self, q_edges):
        for q_edge in q_edges:
            nodes = {
                'subject': q_edge['subject'],
                'object': q_edge['object']
            }
            stripped_curries = []
            for node_type, node in nodes.items():
                reduced_curies = []
                node_stripped_curies = []
                if not node['curie']:
                    return
                for curie in node['curie']:
                    if curie not in reduced_curies:
                        equivalent_already_included = any(equivalent_curie for equivalent_curie in
                                                          q_edge['input_equivalent_identifiers'][curie][0]['curies']
                                                          if equivalent_curie in reduced_curies)
                        if not equivalent_already_included:
                            reduced_curies.append(curie)
                        else:
                            node_stripped_curies.append(curie)
                node['curie'] = reduced_curies
                stripped_curries.append(*node_stripped_curies)
                if len(node_stripped_curies) > 0:
                    pass
            for curie in stripped_curries:
                q_edge['input_equivalent_identifiers'].pop(curie)

    # TODO: q_edges is an empty list when running
    # test_query_to_text_mining_cooccurence_kp_should_be_correctly_paginated test
    # one q_edge should be present
    def query(self, q_edges):
        q_edges = q_edges if isinstance(q_edges, list) else [q_edges]
        node_update = NodesUpdateHandler(q_edges)
        node_update.set_equivalent_ids(q_edges)
        self._rm_equivalent_duplicates(q_edges)

        cache_handler = CacheHandler(q_edges, self.caching, self.kg)
        data = cache_handler.categorize_edges(q_edges)
        cached_results = data['cached_results']
        non_cached_edges = data['non_cached_edges']
        logs = [*self.logs, *cache_handler.logs]

        if len(non_cached_edges) == 0:
            query_res = []
        else:
            edge_converter = QEdge2BTEEdgeHandler(non_cached_edges, self.kg)
            bte_edges = edge_converter.convert(non_cached_edges)
            self.logs = [*self.logs, *edge_converter.logs]
            if len(bte_edges) == 0 and len(cached_results) == 0:
                return []
            expanded_bte_edges = self._expand_bte_edges(bte_edges)
            query_res = self._query_bte_edges(expanded_bte_edges)
            query_res = [res for res in query_res if res]
            cache_handler.cache_edges(query_res)
        query_res = [*query_res, *cached_results]
        node_update.update(query_res)
        return query_res

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers = [fn for fn in self.subscribers if fn != subscriber]

    def notify(self, res):
        for subscriber in self.subscribers:
            subscriber.update(res)
