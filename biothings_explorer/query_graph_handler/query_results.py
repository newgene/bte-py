from collections import ChainMap
import copy
from .helper import QueryGraphHelper
helper = QueryGraphHelper()


class QueryResult:
    def __init__(self):
        self.results = []
        self.cached_query_results = []

    def _add_remaining_cached_query_results(self, previous_input_node_id, results, result, cached_query_result_index=1):
        if cached_query_result_index >= len(self.cached_query_results):
            return results
        cached_query_result = self.cached_query_results[cached_query_result_index]
        for i, cached_record in enumerate(cached_query_result.get(previous_input_node_id)):
            if i > 0:
                result = copy.copy(result)
                results.append(result)
            result['node_bindings'][cached_record['input_query_node_id']] = [
                {
                    'id': cached_record['input_node_id']
                }
            ]
            result['edge_bindings'][cached_record['query_edge_id']] = [
                {
                    'id': cached_record['kg_edge_id']
                }
            ]
            self._add_remaining_cached_query_results(cached_record['input_node_id'], results, result, cached_query_result_index + 1)

    def get_results(self):
        results = []
        for output_node_id, cached_records in self.cached_query_results[0].items():
            for cached_record in cached_records:
                result = {
                    'node_bindings': {
                        cached_record['input_query_node_id']: [
                            {
                                'id': cached_record['input_node_id']
                            }
                        ],
                        cached_record['output_query_node_id']: [
                            {
                                'id': cached_record['output_node_id']
                            }
                        ]
                    },
                    'edge_bindings': {
                        cached_record['query_edge_id']: [
                            {
                                'id': cached_record['kg_edge_id']
                            }
                        ]
                    }
                }
                results.append(result)
                self._add_remaining_cached_query_results(cached_record['input_node_id'], results, result, 1)
        return results

    def _create_node_bindings(self, record):
        return {
            helper._get_input_query_node_id(record): [{'id': helper._get_input_id(record)}],
            helper._get_output_query_node_id(record): [{'id': helper._get_output_id(record)}]
        }

    def _create_edge_bindings(self, record):
        return {
            record['$edge_metadata']['trapi_qEdge_obj'].get_id(): [{'id': helper._get_kg_edge_id(record)}]
        }

    def update(self, query_result):
        if len(self.cached_query_results) > 0:
            previous_cached_query_result = self.cached_query_results[0]
            previous_output_node_ids = set(previous_cached_query_result.keys())
        else:
            previous_output_node_ids = set()

        cached_query_result = ChainMap()

        for record in query_result:
            input_node_id = helper._get_input_id(record)
            output_node_id = helper._get_output_id(record)

            if len(self.cached_query_results) == 0 or input_node_id in previous_output_node_ids:
                if output_node_id in cached_query_result:
                    cached_records_for_output_node_id = cached_query_result.get(output_node_id)
                else:
                    cached_records_for_output_node_id = []
                    cached_query_result[output_node_id] = cached_records_for_output_node_id
                cached_records_for_output_node_id.append({
                    'input_query_node_id': helper._get_input_query_node_id(record),
                    'input_node_id': input_node_id,
                    'query_edge_id': record['$edge_metadata']['trapi_qEdge_obj'].get_id(),
                    'kg_edge_id': helper._get_kg_edge_id(record),
                    'output_query_node_id': helper._get_output_query_node_id(record),
                    'output_node_id': output_node_id,
                })
        # add items to the start of the array
        self.cached_query_results = [*cached_query_result.maps, *self.cached_query_results]
