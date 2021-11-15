from .batch_edge_query import BatchEdgeQueryHandler
from .log_entry import LogEntry
import json


class EdgeManager:
    def __init__(self, edges):
        self.edges = [item for sublist in edges.values() for item in sublist]
        self.logs = []
        self.results = []

    def init(self):
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f"Edge manager is managing {len(self.edges)} edges."
            ).get_log()
        )

    def log_entity_counts(self):
        for edge in self.edges:
            pass

    def pre_send_off_check(self, _next):
        if _next['object']['entity_count'] and _next['subject']['entity_count']:
            _next.choose_lower_entity_value()
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    'Next edge will pick lower entity value to use for query.'
                ).get_log()
            )
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f"Edge manager is sending next edge '{_next.get_id()}' for execution."
            ).get_log()
        )
        self.log_entity_counts()
        return _next

    def get_next(self):
        available_edges = [edge for edge in self.edges if not edge['executed']]
        if len(available_edges) == 0:
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f"Cannot get next edge, {available_edges} available edges found."
                ).get_log()
            )
        lowest_entity_count = None
        _next = None
        current_obj_lowest = 0
        current_sub_lowest = 0
        for edge in available_edges:
            if edge and edge['object']['entity_count']:
                current_obj_lowest = edge['object']['entity_count']
                if not lowest_entity_count:
                    lowest_entity_count = current_obj_lowest
                if current_obj_lowest <= lowest_entity_count:
                    _next = edge
            if edge and edge['subject']['entity_count'] and edge['subject']['entity_count'] > 0:
                current_sub_lowest = edge['subject']['entity_count']
                if not lowest_entity_count:
                    lowest_entity_count = current_sub_lowest
                if current_sub_lowest <= lowest_entity_count:
                    _next = edge
        if not _next:
            all_empty = [edge for edge in available_edges if
                         not edge['object']['entity_count'] and not edge['subject']['entity_count']]
            if len(all_empty) == 0:
                self.logs.append(
                    LogEntry(
                        'DEBUG',
                        None,
                        "Cannot get next edge, No available edges found."
                    ).get_log()
                )
            return all_empty[0]
        return _next

    # def update_edges_entity_counts(self, results, current_edge):
    #     entities = set()
    #     for res in results:
    #         if not isinstance(res['$output'], list) and 'original' in res['$output']:
    #             if not isinstance(res['$output']['original'], list):
    #                 entities.add(res['$output']['original'])
    #     entities = [*entities]
    #     current_node_ids = [current_edge['object']['id'], current_edge['subject']['id']]
    #     for node_id in current_node_ids:
    #         for edge in self.edges:
    #             if node_id in edge['connecting_nodes'] and edge.get_id() != current_edge.get_id():
    #                 edge.update_entity_count_by_id(node_id, entities)

    def get_edges_not_executed(self):
        found = [edge for edge in self.edges if not edge['executed']]
        not_executed = len(found)
        return not_executed

    def _filter_edge_results(self, edge):
        keep = []
        results = edge['results']
        sub_curies = edge['subject']['curie']
        obj_curies = edge['object']['curie']
        object_node_ids = sub_curies if edge['reverse'] else obj_curies
        subject_node_ids = obj_curies if edge['reverse'] else sub_curies

        for res in results:
            ids = set()
            output_match = False
            input_match = False
            for o in res['$input']['obj']:
                if o.get('_dbIDs'):
                    for prefix in o:
                        if isinstance(o['_dbIDs'][prefix], list):
                            for single_alias in o['_dbIDs'][prefix]:
                                if ':' in single_alias:
                                    ids.add(single_alias)
                                else:
                                    ids.add(prefix + ':' + single_alias)
                        else:
                            if ':' in o['_dbIDs'][prefix]:
                                ids.add(o['_dbIDs'][prefix])
                            else:
                                ids.add(prefix + ':' + o['_dbIDs'][prefix])
                elif o.get('curie'):
                    ids.add(o['curie'])
                else:
                    ids.add(res['$input']['original'])
                input_match = len(list(set(*ids) & set(subject_node_ids)))
            o_ids = set()
            for o in res['$output']['obj']:
                if o.get('_dbIDs'):
                    for prefix in o['_dbIDs']:
                        if isinstance(o['_dbIDs'][prefix], list):
                            for single_alias in o['_dbIDs'][prefix]:
                                if ':' in single_alias:
                                    o_ids.add(single_alias)
                                else:
                                    o_ids.add(prefix + ':' + single_alias)
                        else:
                            if ':' in o['_dbIDs'][prefix]:
                                o_ids.add(o['_dbIDs'][prefix])
                            else:
                                o_ids.add(prefix + ':' + o['_dbIDs'][prefix])
                elif o.get('curie'):
                    o_ids.add(o['curie'])
                else:
                    o_ids.add(res['$output']['original'])
                output_match = len(list(set(*o_ids) & set(object_node_ids)))
            if input_match and output_match:
                keep.append(res)
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f"'{edge.get_id()}' kept ({len(keep)}) / dropped ({len(results) - len(keep)}) results."
                ).get_log()
            )
        return keep

    def collect_results(self):
        results = []
        broken_chain = False
        broken_edges = []
        for edge in self.edges:
            filtered_res = edge['results']
            if len(filtered_res) == 0:
                self.logs.append(
                    LogEntry(
                        'DEBUG',
                        None,
                        f"Warning: Edge '{edge.get_id()}' resulted in (0) results."
                    ).get_log()
                )
                broken_chain = True
                broken_edges.append(edge.get_id())
            self.logs = [*self.logs, *edge.logs]
            results = [*results, *filtered_res]
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f"'{edge.get_id()}' keeps ({len(filtered_res)}) results!"
                ).get_log()
            )
            if broken_chain:
                results = []
                self.logs.append(
                    LogEntry(
                        'DEBUG',
                        None,
                        f"Edges {json.dumps(broken_edges)} "
                        f"resulted in (0) results. No complete paths can be formed."
                    ).get_log()
                )
            self.results = results
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f"Edge manager collected ({len(self.results)}) results!"
                ).get_log()
            )

    def update_edge_results(self, current_edge):
        filtered_res = self._filter_edge_results(current_edge)
        current_edge.store_results(filtered_res)

    def update_neighbors_edge_results(self, current_edge):
        not_this_edge = current_edge.get_id()
        left_connections = current_edge['q_edge']['subject'].get_connections()
        left_connections = [edge_id for edge_id in left_connections if edge_id != not_this_edge]
        right_connections = current_edge['q_edge']['object'].get_connections()
        right_connections = [edge_id for edge_id in right_connections if edge_id != not_this_edge]

        if len(left_connections):
            for neighbor_id in left_connections:
                edge = next([edge for edge in self.edges if edge.get_id() == neighbor_id], None)
                if edge and len(edge):
                    self.update_edge_results(edge)
        if len(right_connections):
            for neighbor_id in right_connections:
                edge = next([edge for edge in self.edges if edge.get_id() == neighbor_id], None)
                if edge and len(edge):
                    self.update_edge_results(edge)

    def gather_results(self):
        results = []
        broken_chain = False
        broken_edges = []
        #self.refresh_edges()
        for edge in self.edges:
            filtered_res = self._filter_edge_results(edge)
            if len(filtered_res) == 0:
                self.logs.append(
                    LogEntry(
                        'DEBUG',
                        None,
                        f"Warning: Edge '{edge.get_id()}' resulted in (0) results."
                    ).get_log()
                )
                broken_chain = True
                broken_edges.append(edge.get_id())
            self.logs = [*self.logs, *edge.logs]
            edge.results = filtered_res
            results = [*results, *filtered_res]
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f"'${edge.get_id()}' keeps ({len(filtered_res)}) results!"
                ).get_log()
            )
            self.results = results
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f"Edge manager collected ({len(self.results)}) results!"
                ).get_log()
            )
        if broken_chain:
            results = []
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f'Edges ${json.dumps(broken_edges)} ` + '
                    f'resulted in (0) results. No complete paths can be formed.'
                ).get_log()
            )
        self.results = results
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f"Edge manager collected ({len(self.results)}) results!"
            ).get_log()
        )
