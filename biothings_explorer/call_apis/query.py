import requests
import time
from .builder.builder_factory import builder_factory
from .query_queue import APIQueryQueue
from ..api_response_transform.index import Transformer
from ..biomedical_id_resolver.resolver import generate_invalid_bioentities, resolve_sri, Resolver
from .log_entry import LogEntry


class APIQueryDispatcher:
    def __init__(self, edges):
        for count, edge in enumerate(edges):
            if not isinstance(edges[count]['query_operation'], dict):
                edges[count]['query_operation'] = edges[count]['query_operation'].__dict__
                for key in list(edges[count]['query_operation']):
                    value = edges[count]['query_operation'].pop(key)
                    if key.startswith('_'):
                        key = key[1:]
                    edges[count]['query_operation'][key] = value
        self.edges = edges
        self.logs = []

    def _query_bucket(self, queries):
        res = []
        for query in queries:
            config = query.get_config()
            if 'arax.ncats.io' in config['url']:
                time.sleep(1)
            if config['method'].lower() == 'get':
                request_func = requests.get
            else:
                request_func = requests.post
            config.pop('method')
            try:
                response = request_func(**config)
                try:
                    if response.status_code == 400:
                        res.append(None)
                        continue
                    # TODO
                    # find out why code lands here
                    if response.status_code == 422:
                        pass
                    data = response.json()
                except Exception as e:
                    print(e)
                    res.append(None)
                    continue
            except Exception as e:
                self.logs.append(LogEntry("ERROR", None, f"call-apis: Failed to make to following query: {str(config)}. The error is {str(e)}").get_log())
                continue
            edge = query.edge
            if query.need_pagination(data):
                self.logs.append(LogEntry("DEBUG", None, "call-apis: This query needs to be paginated").get_log())
            #self.logs.append(LogEntry("DEBUG", None, f"call-apis: Succesfully made the following query: {str(query['config'])}").get_log())
            tf_obj = Transformer({'response': data, 'edge': edge})
            # TODO
            # data can sometimes have values like 'msg': 'field required' instead of actual data
            # if this is the case the below function returns None
            transformed = tf_obj.transform()
            try:
                self.logs.append(LogEntry("DEBUG", None, f"call-apis: After transformation, BTE is able to retrieve: {len(transformed)} hits!").get_log())
            except Exception as e:
                print(e)
                pass
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
            try:
                if res['status'] == 'fulfilled' and res['value']:
                    result = [*result, *res['value']]
            except Exception as e:
                if res:
                    result = [*result, *res]
        self.logs.append(LogEntry("DEBUG", None, f"call-apis: Total number of results returned for this query is {len(result)}").get_log())
        return result

    def _group_output_ids_by_semantic_type(self, result):
        output_ids = {}
        for item in result:
            if item and item['$edge_metadata']:
                output_type = item['$edge_metadata'].get('output_type')
                if output_type not in output_ids:
                    output_ids[output_type] = []
                output_ids[output_type].append(item['$output'].get('original'))
        return output_ids

    def _annotate(self, result, enable=True):
        grped_ids = self._group_output_ids_by_semantic_type(result)
        if not enable:
            res = generate_invalid_bioentities(grped_ids)
        else:
            res = resolve_sri(grped_ids)
        for item in result:
            if item:
                item['$output']['obj'] = res[item['$output']['original']]
        return result
