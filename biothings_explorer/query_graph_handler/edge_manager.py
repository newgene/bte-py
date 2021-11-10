from .batch_edge_query import BatchEdgeQueryHandler
from .log_entry import LogEntry


class EdgeManager:
    def __init__(self, edges):
        self.edges = [item for sublist in edges.values() for item in sublist]
        self.logs = []
        self.results = []

    def init(self):
        pass

    def log_entity_counts(self):
        for edge in self.edges:
            pass

    def refresh_edges(self):
        for edge in self.edges:
            edge.update_entity_counts()

    def pre_send_off_check(self, _next):
        if _next['requires_entity_count_choice']:
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
                f"Edge manager is sending next edge {_next.get_id()} for execution."
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
            if edge and edge['object_entity_count']:
                current_obj_lowest = edge['object_entity_count']
                if not lowest_entity_count:
                    lowest_entity_count = current_obj_lowest
                if current_obj_lowest <= lowest_entity_count:
                    _next = edge
            if edge and edge['subject_entity_count'] and edge['subject_entity_count'] > 0:
                current_sub_lowest = edge['subject_entity_count']
                if not lowest_entity_count:
                    lowest_entity_count = current_sub_lowest
                if current_sub_lowest <= lowest_entity_count:
                    _next = edge
        if not _next:
            all_empty = [edge for edge in available_edges if
                         not edge['object_entity_count'] and not edge['subject_entity_count']]
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

    def _reduce_edge_results_with_neighbor_edge(self, edge, neighbor):
        first = edge['results']
        second = neighbor['results']
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f"Edge manager will try to intersect ({len(first)}) & ({len(second)}) results"
            ).get_log()
        )
        results = []
        dropped = 0
        for f in first:
            first_semantic_types = f['$input']['obj']
            first_semantic_types = first_semantic_types + f['$output']['obj']
            for f_type in first_semantic_types:
                for s in second:
                    second_semantic_types = s['$input']['obj']
                    second_semantic_types = second_semantic_types + s['$output']['obj']
                    for s_type in second_semantic_types:
                        if f_type['_leafSemanticType'] == s_type['_leafSemanticType']:
                            f_ids = set()
                            for prefix in f_type['_dbIDs']:
                                f_ids.add(prefix + ':' + f_type['_dbIDs'][prefix])
                            f_ids = [*f_ids]
                            s_ids = set()
                            for prefix in s_type['_dbIDs']:
                                s_ids.add(prefix + ':' + s_type['_dbIDs'][prefix])
                            s_ids = [*s_ids]
                            shares_ids = len(list(set(f_ids) & set(s_ids)))
                            if shares_ids:
                                results.append(f)
        dropped = len(first) - len(results)
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f'Edge manager is intersecting results for "{edge.get_id()}" Kept ({len(results)}) / Dropped ({dropped})'
            ).get_log()
        )
        if len(results) == 0:
            self.logs.append(
                LogEntry(
                    'DEBUG',
                    None,
                    f'After intersection of "{edge.get_id()}" and "{neighbor.get_id()}" edge manager got 0 results.'
                ).get_log()
            )
        return results

    def gather_results_old(self):
        for index, edge in enumerate(self.edges):
            neighbor = self.edges[index + 1]
            if not neighbor:
                current = self._reduce_edge_results_with_neighbor_edge(edge, neighbor)
                edge.store_results(current)
                _next = self._reduce_edge_results_with_neighbor_edge(neighbor, edge)
                neighbor.store_results(_next)
                self.logs.append(
                    LogEntry(
                        'DEBUG',
                        None,
                        f'"${edge.get_id()}" keeps ({len(current)}) results and "${neighbor.getID()}" keeps ({len(_next)}) results!'
                    ).get_log()
                )
        for edge in self.edges:
            for r in edge['results']:
                self.results.append(r)
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f'Edge manager collected ({len(self.results)}) results!'
            ).get_log()
        )

    def gather_results(self):
        for edge in self.edges:
            current = self._filter_edge_results(edge)
            edge['results'] = current
        for edge in self.edges:
            for r in edge['results']:
                self.results.append(r)

        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f'Edge manager collected ({len(self.results)}) results!'
            ).get_log()
        )

    def _filter_edge_results(self, edge):
        keep = []
        results = edge['results']
        sub_curies = edge['subject']['curie']
        obj_curies = edge['object']['curie']
        objs = sub_curies if edge['reverse'] else obj_curies
        subs = obj_curies if edge['reverse'] else sub_curies

        for res in results:
            ids = set()
            output_match = False
            input_match = False
            for o in res['$input']['obj']:
                for prefix in o['_dbIDs']:
                    ids.add(prefix + ':' + o['_dbIDs'][prefix])
                input_match = len(list(set(*ids) & set(subs)))
            o_ids = set()
            for o in res['$output']['obj']:
                for prefix in o['_dbIDs']:
                    o_ids.add(prefix + ':' + o['_dbIDs'][prefix])
                output_match = len(list(set(*o_ids) & set(objs)))
            if input_match and output_match:
                keep.append(res)
        return keep
