import functools
from .helper import QueryGraphHelper
helper = QueryGraphHelper()


def to_pairs(obj):
    return [[key, value] for key, value in obj.items()]


class QueryResult:
    def __init__(self):
        self._results = []

    def get_results(self):
        return self._results

    def update(self, data_by_edge):
        self._results = []
        edges = set(data_by_edge.keys())
        edge_count = len(edges)
        common_primary_ids_by_query_node_id = {}
        empty_query_node_found = False

        for item in to_pairs(data_by_edge):
            query_edge_id = item[0]
            connected_to = item[1]['connected_to']
            records = item[1]['records']
            if not records or len(records) == 0:
                empty_query_node_found = True
                return True
            input_query_node_id = helper._get_input_query_node_id(records[0])
            output_query_node_id = helper._get_output_query_node_id(records[0])
            input_primary_ids = []
            for record in set(records):
                input_primary_ids.append(helper._get_input_id(record))

            if not common_primary_ids_by_query_node_id.get(input_query_node_id):
                common_primary_ids_by_query_node_id[input_query_node_id] = input_primary_ids
            else:
                common_primary_ids_by_query_node_id[input_query_node_id] = \
                    list(set(common_primary_ids_by_query_node_id[input_query_node_id]) & set(input_primary_ids))

            output_primary_ids = []
            for record in set(records):
                output_primary_ids.append(helper._get_output_id(record))

            if not common_primary_ids_by_query_node_id.get(output_query_node_id):
                common_primary_ids_by_query_node_id[output_query_node_id] = output_primary_ids
            else:
                common_primary_ids_by_query_node_id[output_query_node_id] = \
                    list(set(common_primary_ids_by_query_node_id[output_query_node_id]) & set(output_primary_ids))

            if len(common_primary_ids_by_query_node_id[input_query_node_id]) == 0 or len(common_primary_ids_by_query_node_id[output_query_node_id]) == 0:
                empty_query_node_found = True
                return True

        if empty_query_node_found:
            return

        pairs_brief_records_by_edge = to_pairs(data_by_edge)

        def _reduce(acc, curr):
            acc[curr[0]] = [{
                'input_query_node_id': helper._get_input_query_node_id(_record),
                'output_query_node_id': helper._get_output_query_node_id(_record),
                'input_primary_id': helper._get_input_id(_record),
                'output_primary_id': helper._get_output_query_node_id(_record),
                'kg_edge_id': helper._get_kg_edge_id(_record),
            } for _record in curr[1]['records']]
            return acc

        brief_records_by_edge = functools.reduce(
            lambda prev, current: _reduce(prev, current), pairs_brief_records_by_edge, {})

        query_node_ids = common_primary_ids_by_query_node_id.keys()
