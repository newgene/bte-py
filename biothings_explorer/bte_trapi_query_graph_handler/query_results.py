from .helper import QueryGraphHelper
helper = QueryGraphHelper()


class QueryResult:
    def __init__(self):
        self.results = []

    def get_results(self):
        return self.results

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
        for record in query_result:
            self.results.append({
                'node_bindings': self._create_node_bindings(record),
                'edge_bindings': self._create_edge_bindings(record),
            })
