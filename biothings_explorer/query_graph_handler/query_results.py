import functools
from .helper import QueryGraphHelper
from .utils import cartesian, intersection

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

            # TODO better to use set(records) but dicts are unhashable
            for record in records:
                input_primary_ids.append(helper._get_input_id(record))

            if not common_primary_ids_by_query_node_id.get(input_query_node_id):
                common_primary_ids_by_query_node_id[input_query_node_id] = input_primary_ids
            else:
                common_primary_ids_by_query_node_id[input_query_node_id] = \
                    list(set(common_primary_ids_by_query_node_id[input_query_node_id]) & set(input_primary_ids))

            output_primary_ids = []

            # TODO better to use set(records) but dicts are unhashable
            for record in records:
                output_primary_ids.append(helper._get_output_id(record))

            if not common_primary_ids_by_query_node_id.get(output_query_node_id):
                common_primary_ids_by_query_node_id[output_query_node_id] = output_primary_ids
            else:
                common_primary_ids_by_query_node_id[output_query_node_id] = \
                    list(set(common_primary_ids_by_query_node_id[output_query_node_id]) & set(output_primary_ids))

            if len(common_primary_ids_by_query_node_id[input_query_node_id]) == 0 or len(
                    common_primary_ids_by_query_node_id[output_query_node_id]) == 0:
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
                'output_primary_id': helper._get_output_id(_record),
                'kg_edge_id': helper._get_kg_edge_id(_record),
            } for _record in curr[1]['records']]
            return acc

        brief_records_by_edge = functools.reduce(
            lambda prev, current: _reduce(prev, current), pairs_brief_records_by_edge, {})

        query_node_ids = common_primary_ids_by_query_node_id.keys()
        self._results = [list(v) for v in cartesian(common_primary_ids_by_query_node_id.values())]

        # zipping
        self._results = [list(zip(query_node_ids, common_primary_id_combo)) for common_primary_id_combo in self._results]
        # self._results looks like this now [('Candice', 2), ('Ava', 9), ('Andrew', 18), ('Lucas', 28)]
        # but we need dicts instead of tuples

        zipped_lists = []
        for item in self._results:
            node_id = {}
            for zipped_item in item:
                node_id[zipped_item[0]] = zipped_item[1]
                #new_list.append({zipped_item[0]: zipped_item[1]})
            zipped_lists.append(node_id)
        self._results = zipped_lists

        def _reduce_2(acc, curr, primary_id_by_query_node_id):
            compatible_brief_records = [brief_record
                                        for brief_record in curr[1] if
                                        primary_id_by_query_node_id.get(brief_record['input_query_node_id']) == brief_record[
                                            'input_primary_id'] and

                                        primary_id_by_query_node_id.get(brief_record['output_query_node_id']) == brief_record[
                                            'output_primary_id']
                                        ]
            if len(compatible_brief_records) == 0:
                return acc

            def recuce_kg_edge_ids(prev, current):
                prev.add(current['kg_edge_id'])
                return prev

            kg_edge_ids = functools.reduce(lambda prev, current: recuce_kg_edge_ids(prev, current),
                                           compatible_brief_records, set())

            acc[query_edge_id] = {
                'input_query_node_id': compatible_brief_records[0]['input_query_node_id'],
                'output_query_node_id': compatible_brief_records[0]['output_query_node_id'],
                'input_primary_id': compatible_brief_records[0]['input_primary_id'],
                'output_primary_id': compatible_brief_records[0]['output_primary_id'],
                'kg_edge_ids': kg_edge_ids
            }

            return acc
        self._results = [functools.reduce(lambda prev, curr: _reduce_2(prev, curr, primary_id_by_query_node_id),
                                          to_pairs(brief_records_by_edge), {})
                         for primary_id_by_query_node_id in self._results]

        self._results = [info_by_edge_for_one_combo for info_by_edge_for_one_combo in self._results if
                         len(intersection(edges, set(info_by_edge_for_one_combo.keys()))) == edge_count]
        new_results = []
        for info_by_edge_for_one_combo in self._results:
            result = {'node_bindings': {}, 'edge_bindings': {}, 'score': '1.0'}
            for item in to_pairs(info_by_edge_for_one_combo):
                query_edge_id = item[0]
                input_query_node_id = item[1]['input_query_node_id']
                output_query_node_id = item[1]['output_query_node_id']
                input_primary_id = item[1]['input_primary_id']
                output_primary_id = item[1]['output_primary_id']
                kg_edge_ids = item[1]['kg_edge_ids']

                if not result['node_bindings'].get(input_query_node_id):
                    result['node_bindings'][input_query_node_id] = [
                        {
                            'id': input_primary_id
                        }
                    ]

                if not result['node_bindings'].get(output_query_node_id):
                    result['node_bindings'][output_query_node_id] = [
                        {
                            'id': output_primary_id
                        }
                    ]

                result['edge_bindings'][query_edge_id] = result['edge_bindings'].get(query_edge_id) \
                    if result['edge_bindings'].get(query_edge_id) else []
                edge_bindings = result['edge_bindings'][query_edge_id]
                for kg_edge_id in kg_edge_ids:
                    edge_bindings.append({'id': kg_edge_id})
            new_results.append(result)
        self._results = new_results
