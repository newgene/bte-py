from .batch_edge_query import BatchEdgeQueryHandler
from .exceptions.bte_error import BTEError
from .log_entry import LogEntry
from .config import ENTITY_MAX
import json


class EdgeManager:
    def __init__(self, edges):
        self.edges = [item for sublist in edges.values() for item in sublist]
        self.logs = []
        self.results = []
        self.organized_results = {}
        self.init()

    def init(self):
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f"Edge manager is managing {len(self.edges)} edges."
            ).get_log()
        )

    def get_results(self):
        return self.results

    def get_organized_results(self):
        return self.organized_results

    def log_entity_counts(self):
        for edge in self.edges:
            pass

    def pre_send_off_check(self, _next):
        self.check_entity_max(_next)
        if _next['object']['entity_count'] and _next['subject']['entity_count']:
            _next.choose_lower_entity_value()
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    'Next edge will pick lower entity value to use for query.'
                ).get_log()
            )
        elif _next['object']['entity_count'] and not _next['subject']['entity_count'] or \
                not _next['object']['entity_count'] and not _next['subject']['entity_count']:
            _next['reverse'] = False if _next['subject_entity_count'] else True
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
            return self.pre_send_off_check(all_empty[0])
        return self.pre_send_off_check(_next)

    def check_entity_max(self, _next):
        _max = ENTITY_MAX
        sub_count = _next['object'].get_entity_count()
        obj_count = _next['subject'].get_entity_count()

        if obj_count == 0 and sub_count > _max or obj_count > _max and \
            sub_count == 0 or obj_count > _max and sub_count > _max:
            raise BTEError(f"Max number of entities exceeded ({_max}) in '{_next.get_id()}'")

    def get_edges_not_executed(self):
        found = [edge for edge in self.edges if not edge['executed']]
        not_executed = len(found)
        return not_executed

    def _filter_edge_results(self, edge):
        keep = []
        results = edge['results']
        sub_count = edge['subject']['curie']
        obj_count = edge['object']['curie']
        object_node_ids = sub_count if edge['reverse'] else obj_count
        subject_node_ids = obj_count if edge['reverse'] else sub_count

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
        results = {}
        combined_results = []
        broken_chain = False
        broken_edges = []
        for edge in self.edges:
            edge_id = edge.get_id()
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
            combined_results = [*combined_results, *filtered_res]
            connections = [*edge['q_edge']['subject'].get_connections(), edge['q_edge']['object'].get_connections()]
            connections = [_id for _id in connections if _id != edge_id]
            connections = set(connections)
            results[edge_id] = {
                'records': filtered_res,
                'connected_to': [*connections]
            }
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f"'{edge.get_id()}' keeps ({len(filtered_res)}) results!"
                ).get_log()
            )
        if broken_chain:
            results = {}
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f"Edges {json.dumps(broken_edges)} "
                    f"resulted in (0) results. No complete paths can be formed."
                ).get_log()
            )
        self.organized_results = results
        self.results = combined_results
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

    def update_all_other_edges(self, current_edge):
        not_this_edge = current_edge.get_id()
        for edge in self.edges:
            if edge.get_id() != not_this_edge and len(edge.results):
                self.update_edge_results(edge)
                self.update_edge_results(current_edge)
