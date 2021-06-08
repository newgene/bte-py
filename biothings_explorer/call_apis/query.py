import requests
from .builder.builder_factory import builder_factory
from .query_queue import APIQueryQueue
from ..api_response_transform.index import Transformer
from ..biomedical_id_resolver.biolink import BioLink
from .log_entry import LogEntry


class APIQueryDispatcher:
    def __init__(self, edges):
        self.edges = edges
        self.logs = []

    def _query_bucket(self, queries):
        res = []
        for query in queries:
            # TODO add try except
            config = query.get_config()
            if config['method'].lower() == 'get':
                request_func = requests.get
            else:
                request_func = requests.post
            response = request_func(**config)
            data = response.json()
            edge = query['edge']
            if query.need_pagination(data):
                self.logs.append(LogEntry("DEBUG", None, "call-apis: This query needs to be paginated").get_log())
            self.logs.append(LogEntry("DEBUG", None, f"call-apis: Succesfully made the following query: {str(query['config'])}").get_log())
            tf_obj = Transformer({'response': data, 'edge': edge})
            transformed = tf_obj.transform()
            self.logs.append(LogEntry("DEBUG", None, f"call-apis: After transformation, BTE is able to retrieve: {len(transformed)} hits!").get_log())
            res.append(transformed)
        self.queue.dequeue()
        return res

    def _check_if_next(self, queries):
        for query in queries:
            if query.has_next:
                self.queue.add_query(query)

    def _construct_queries(self, edges):
        return [builder_factory(edge) for edge in edges]

    def _construct_queue(self, queries):
        self.queue = APIQueryQueue(queries)
        self.queue.construct_queue(queries)

    def query(self, resolve_output_ids=True):
        self.logs.append(LogEntry("DEBUG", None, f"call-apis: Resolving ID feature is turned {'on' if resolve_output_ids else 'off'}").get_log())
        self.logs.append(LogEntry("DEBUG", None, f"call-apis: Number of BTE Edges received is {len(self.edges)}").get_log())
        query_result = []
        queries = self._construct_queries(self.edges)
        self._construct_queue(queries)
        while len(self.queue.queue) > 0:
            bucket = self.queue.queue[0].get_bucket()
            res = self._query_bucket(bucket)
            query_result = [*query_result, *res]
            self._check_if_next(bucket)
        merged_result = self._merge(query_result)
        annotated_result = self._annotate(merged_result, resolve_output_ids)
        self.logs.append(LogEntry("DEBUG", None, f"call-apis: Query completes").get_log())
        return annotated_result

    def _merge(self, query_result):
        result = []
        for res in query_result:
            if res:
                result = [*result, *res]
        self.logs.append(LogEntry("DEBUG", None, f"call-apis: Total number of results returned for this query is {len(result)}").get_log())
        return result