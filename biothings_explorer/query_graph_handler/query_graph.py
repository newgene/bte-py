from .query_node import QNode
from .query_node_2 import QNode as QNode2
from .query_edge import QEdge
from .query_execution_edge import QExeEdge
from .log_entry import LogEntry
from .exceptions.invalid_query_graph_error import InvalidQueryGraphError
MAX_DEPTH = 3


class QueryGraphHandler:
    def __init__(self, query_graph):
        self.query_graph = query_graph
        self.logs = []

    def _validate_empty_nodes(self, query_graph):
        if len(query_graph['nodes']) == 0:
            raise InvalidQueryGraphError('Your Query Graph has no nodes defined.')

    def _validate_empty_edges(self, query_graph):
        if len(query_graph['edges']) == 0:
            raise InvalidQueryGraphError('Your Query Graph has no edges defined.')

    def _validate_node_edge_correspondence(self, query_graph):
        for edge_id in query_graph['edges']:
            if self.query_graph['edges'][edge_id]['subject'] not in query_graph['nodes']:
                raise InvalidQueryGraphError(f"The subject of edge {edge_id} is not defined in the query graph.")
            if self.query_graph['edges'][edge_id]['object'] not in query_graph['nodes']:
                raise InvalidQueryGraphError(f"The object of edge {edge_id} is not defined in the query graph.")

    def _validate(self, query_graph):
        self._validate_empty_edges(query_graph)
        self._validate_empty_nodes(query_graph)
        self._validate_node_edge_correspondence(query_graph)

    def _store_nodes(self):
        nodes = {}
        for node_id in self.query_graph['nodes']:
            nodes[node_id] = QNode(node_id, self.query_graph['nodes'][node_id])
        self.logs.append(
            LogEntry('DEBUG', None, f"BTE identified {len(nodes)} QNodes from your query graph").get_log()
        )
        return nodes

    def _store_edges(self):
        if not hasattr(self, 'nodes'):
            self.nodes = self._store_nodes()
        edges = {}
        for edge_id in self.query_graph['edges']:
            edge_info = {
                **self.query_graph['edges'][edge_id],
                **{
                    'subject': self.nodes[self.query_graph['edges'][edge_id]['subject']],
                    'object': self.nodes[self.query_graph['edges'][edge_id]['object']]
                }
            }

            edges[edge_id] = QEdge(edge_id, edge_info)
            self.logs.append(
                LogEntry('DEBUG', None, f"BTE identified {len(edges)} QEdges from your query graph").get_log()
            )
        return edges

    def _store_nodes_2(self):
        nodes = {}
        for node_id in self.query_graph['nodes']:
            nodes[node_id] = QNode2(node_id, self.query_graph['nodes'][node_id])
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f"BTE identified {len(nodes.keys())} QNodes from your query graph"
            ).get_log()
        )
        return nodes

    def _store_edges_2(self):
        if not self.nodes:
            self.nodes = self._store_nodes_2()
        edges = {}
        for edge_id in self.query_graph['edges']:
            edge_info = {
                **self.query_graph['edges'][edge_id],
                'subject': self.nodes[self.query_graph['edges'][edge_id]['subject']],
                'object': self.nodes[self.query_graph['edges'][edge_id]['object']]
            }
            self.nodes[self.query_graph['edges']['subject']].update_connection(edge_id)
            self.nodes[self.query_graph['edges']['object']].update_connection(edge_id)
            edges[edge_id] = QEdge(edge_id, edge_info)
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f"BTE identified {len(edges.keys())} QEdges from your query graph"
            ).get_log()
        )
        return edges

    def create_query_paths(self):
        self._validate(self.query_graph)
        paths = {}
        current_graph = self._find_first_level_edges()
        paths[0] = [item['edge'] for item in current_graph]
        for i in range(1, MAX_DEPTH + 1):
            current_graph = self._find_next_level_edges(current_graph)
            if len(current_graph) > 0 and i == MAX_DEPTH:
                raise InvalidQueryGraphError(f"Your Query Graph exceeds the maximum query depth set in bte, which is {MAX_DEPTH}")
            if len(current_graph) == 0:
                break
            paths[i] = [item['edge'] for item in current_graph]
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f"BTE identified your query graph as a {len(paths)} -depth query graph"
            ).get_log()
        )
        return paths

    def _find_first_level_edges(self):
        if not hasattr(self, 'edges'):
            self.edges = self._store_edges()
        result = []
        for edge_id in self.edges:
            subject_node = self.edges[edge_id].subject
            object_node = self.edges[edge_id].object
            if subject_node.has_input():
                result.append({
                    'current_node': object_node,
                    'edge': QExeEdge(self.edges[edge_id], False, None),
                    'path_source_node': subject_node,
                })
            if object_node.has_input():
                result.append({
                    'current_node': subject_node,
                    'edge': QExeEdge(self.edges[edge_id], True, None),
                    'path_source_node': object_node,
                })
        return result

    def _find_next_level_edges(self, groups):
        result = []
        for edge in self.edges.values():
            for grp in groups:
                if edge.get_id() != grp['edge'].get_id():
                    if edge.subject.get_id() == grp['current_node'].get_id():
                        result.append({
                            'current_node': edge.object,
                            'edge': QExeEdge(edge, False, grp['edge']),
                            'path_source_node': grp['path_source_node']
                        })
                    elif edge.object.get_id() == grp['current_node'].get_id():
                        result.append({
                            'current_node': edge.subject,
                            'edge': QExeEdge(edge, True, grp['edge']),
                            'path_source_node': grp['path_source_node'],
                        })
        return result
