from biothings_explorer.call_apis.query import APIQueryDispatcher
from .qedge2bteedge import QEdge2BTEEdgeHandler
from .update_nodes import NodesUpdateHandler
from .cache_handler import CacheHandler
from .utils import to_array, remove_biolink_prefix


class BatchEdgeQueryHandler:
    def __init__(self, kg, resolve_output_ids=True):
        self.kg = kg
        self.subscribers = []
        self.logs = []
        self.resolve_output_ids = resolve_output_ids

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
        try:
            filtered = []
            for item in response:
                edge_predicate = item['$edge_metadata']['predicate']
                predicate_filters = item['$edge_metadata']['trapi_qEdge_obj']['qEdge']['predicate']
                predicate_filters = [remove_biolink_prefix(item) for item in predicate_filters]
                if edge_predicate in predicate_filters:
                    filtered.append(item)
            return filtered
        except Exception as e:
            print(e)
            return response

    def query(self, q_edges):
        node_update = NodesUpdateHandler(q_edges)
        node_update.set_equivalent_ids(q_edges)
        cache_handler = CacheHandler(q_edges)
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
            cache_handler.cache_edges(query_res)
        query_res = [*query_res, *cached_results]
        processed_query_res = self._post_query_filter(query_res)
        node_update.update(processed_query_res)
        return processed_query_res

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers = [fn for fn in self.subscribers if fn != subscriber]

    def notify(self, res):
        for subscriber in self.subscribers:
            subscriber.update(res)
