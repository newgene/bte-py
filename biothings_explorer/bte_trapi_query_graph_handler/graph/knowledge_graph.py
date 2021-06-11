from ..helper import QueryGraphHelper
helper = QueryGraphHelper()


class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.kg = {
            'nodes': self.nodes,
            'edges': self.edges,
        }

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def _create_node(self, kg_node):
        res = {
            'category': 'biolink:' + kg_node._semantic_type,
            'name': kg_node._label,
            'attributes': [
                {
                    'attribute_type_id': 'equivalent_identifiers',
                    'value': kg_node._curies,
                    'type': 'biolink:id'
                },
                {
                    'attribute_type_id': 'num_source_nodes',
                    'value': len(kg_node._source_nodes),
                    'type': 'bts:num_source_nodes'
                },
                {
                    'attribute_type_id': 'num_target_nodes',
                    'value': len(kg_node._target_nodes),
                    'type': 'bts:num_target_nodes'
                },
                {
                    'attribute_type_id': 'source_qg_nodes',
                    'value': [item for item in kg_node._source_qg_nodes],
                    'type': 'bts:source_qg_nodes'
                },
                {
                    'attribute_type_id': 'target_qg_nodes',
                    'value': [item for item in kg_node._target_qg_nodes],
                    'type': 'bts:target_qg_nodes'
                },
            ]
        }
        for key in kg_node._node_attributes:
            res['attributes'].append({
                'attribute_type_id': key,
                'value': kg_node._node_attributes[key],
                'type': 'bts:' + key
            })
        return res

    def _create_attributes(self, kg_edge):
        attributes = [
            {
                'attribute_type_id': 'provided_by',
                'value': [item for item in kg_edge.sources],
                'type': 'biolink:provided_by'
            },
            {
                'attribute_type_id': 'api',
                'value': [item for item in kg_edge.apis],
                'type': 'bts:api'
            },
            {
                'attribute_type_id': 'publications',
                'value': [item for item in kg_edge.publications],
                'type': 'biolink:publication'
            },
        ]
        for key in kg_edge.attributes:
            attributes.append({
                'attribute_type_id': key,
                'value': kg_edge.attributes[key],
                'type': 'bts:' + key,
            })
        return attributes

    def _create_edge(self, kg_edge):
        return {
            'predicate': kg_edge.predicate,
            'subject': kg_edge.subject,
            'object': kg_edge.object,
            'attributes': self._create_attributes(kg_edge)
        }

    def update(self, bte_graph):
        for node in bte_graph.nodes:
            self.nodes[bte_graph.nodes[node]._primary_id] = self._create_node(bte_graph.nodes[node])
        for edge in bte_graph.edges:
            self.edges[edge] = self._create_node(bte_graph.edges[edge])
        self.kg = {
            'nodes': self.nodes,
            'edges': self.edges,
        }
