import json
import os
from dotenv import load_dotenv
from .redis_client import client, enable_redis
from .log_entry import LogEntry

load_dotenv()


class CacheHandler:
    def __init__(self, q_edges, logs=[]):
        self.q_edges = q_edges
        self.logs = logs
        self.cache_enabled = enable_redis
        self.logs.append(
            LogEntry('DEBUG', None, f"REDIS cache is {'' if self.cache_enabled else 'not'} enabled")
        )

    def categorize_edges(self, q_edges):
        if not self.cache_enabled:
            return {
                'cached_results': [],
                'non_cached_edges': q_edges
            }
        non_cached_edges = []
        cached_results = []
        for edge in q_edges:
            hashed_edge_id = edge.get_hashed_edge_representation()
            cached_res = client.get(hashed_edge_id)
            cached_res_json = json.loads(cached_res)
            if cached_res_json:
                self.logs.append(LogEntry('DEBUG', None, f'BTE find cached results for {edge.get_id()}').get_log())
                for rec in cached_res_json:
                    rec['$edge_metadata']['trapi_qEdge_obj'] = edge
                cached_results = [*cached_results, *cached_res_json]
            else:
                non_cached_edges.append(edge)

        return {
            'cached_results': cached_results,
            'non_cached_edges': non_cached_edges,
        }

    def _copy_record(self, record):
        new_record = {
            '$edge_metadata': {
                'input_id': record['$edge_metadata']['input_id'],
                'output_id': record['$edge_metadata']['output_id'],
                'output_type': record['$edge_metadata']['output_type'],
                'input_type': record['$edge_metadata']['input_type'],
                'predicate': record['$edge_metadata']['predicate'],
                'source': record['$edge_metadata']['source'],
                'api_name': record['$edge_metadata']['api_name']
            },
            '$input': {
                'original': record['$input']['original'],
                'obj': [
                    {
                        'db_ids': record['$input']['obj'][0]['db_ids'],
                        'curies': record['$input']['obj'][0]['curies'],
                        'label': record['$input']['obj'][0]['label'],
                        'primary_id': record['$input']['obj'][0]['primary_id']
                    }
                ]
            },
            '$output': {
                'original': record['$output']['original'],
                'obj': [
                    {
                        'db_ids': record['$output']['obj'][0]['db_ids'],
                        'curies': record['$output']['obj'][0]['curies'],
                        'label': record['$output']['obj'][0]['label'],
                        'primary_id': record['$output']['obj'][0]['primary_id']
                    }
                ]
            }
        }
        for k in record:
            if k not in ['$edge_metadata', '$input', '$output']:
                new_record[k] = record[k]
        return new_record

    def _group_query_results_by_edge_id(self, query_result):
        grouped_result = {}
        for record in query_result:
            hashed_edge_id = record['$edge_metadata']['trapi_qEdge_obj'].get_hashed_edge_representation()
            if hashed_edge_id not in grouped_result:
                grouped_result[hashed_edge_id] = []
            grouped_result[hashed_edge_id].append(self._copy_record(record))
        return grouped_result

    def cache_edges(self, query_result):
        if not self.cache_enabled:
            return None
        grouped_query_result = self._group_query_results_by_edge_id(query_result)
        hashed_edge_ids = list(grouped_query_result.keys())
        for _id in hashed_edge_ids:
            client.setex(_id, os.getenv('REDIS_KEY_EXPIRE_TIME'), json.dumps(grouped_query_result[_id]))
