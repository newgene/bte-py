from .batch_edge_query import BatchEdgeQueryHandler


class EdgeManager:
    def __init__(self, edges, kg):
        self.edges = [item for sublist in edges.values() for item in sublist]
        self.kg = kg
        self.resolve_output_ids = True
        self.logs = []
        self.results = []

    def get_next(self):
        available_edges = [edge for edge in self.edges if not edge['executed']]
        if len(available_edges) == 0:
            pass
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
            all_empty = [edge for edge in available_edges if not edge['object_entity_count'] and not edge['subject_entity_count']]
            if len(all_empty) == 0:
                pass
            return all_empty[0]
        return _next

    def update_edges_entity_counts(self, results, current_edge):
        entities = set()
        for res in results:
            if not isinstance(res['$output'], list) and 'original' in res['$output']:
                if not isinstance(res['$output']['original'], list):
                    entities.add(res['$output']['original'])
        entities = [*entities]
        current_node_ids = [current_edge['object']['id'], current_edge['subject']['id']]
        for node_id in current_node_ids:
            for edge in self.edges:
                if node_id in edge['connecting_nodes'] and edge.get_id() != current_edge.get_id():
                    edge.update_entity_count_by_id(node_id, entities)

    def get_edges_not_executed(self):
        found = [edge for edge in self.edges if not edge['executed']]
        not_executed = len(found)
        return not_executed

    def _reduce_edge_results_with_neighbor_edge(self, edge, neighbor):
        first = edge['results']
        second = neighbor['results']
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
        return results

    def gather_results(self):
        for index, edge in enumerate(self.edges):
            neighbor = self.edges[index + 1]
            if not neighbor:
                current = self._reduce_edge_results_with_neighbor_edge(edge, neighbor)
                edge.store_results(current)
                _next = self._reduce_edge_results_with_neighbor_edge(neighbor, edge)
                neighbor.store_results(_next)
        for edge in self.edges:
            for r in edge['results']:
                self.results.append(r)
