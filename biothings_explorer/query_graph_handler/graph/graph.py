from .kg_edge import KGEdge
from .kg_node import KGNode
from ..helper import QueryGraphHelper


class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.paths = {}
        self.helper = QueryGraphHelper()
        self.subscribers = []

    def update(self, query_result):
        bte_attributes = ['name', 'label', 'id', 'api', 'provided_by', 'publications']
        if len(query_result):
            for record in query_result:
                if record:
                    input_primary_id = self.helper._get_input_id(record)
                    input_qg_id = self.helper._get_input_query_node_id(record)
                    input_id = input_primary_id + '-' + input_qg_id
                    output_primary_id = self.helper._get_output_id(record)
                    output_qg_id = self.helper._get_output_query_node_id(record)
                    output_id = output_primary_id + '-' + output_qg_id
                    edge_id = self.helper._get_kg_edge_id(record)
                    if output_id not in self.nodes:
                        self.nodes[output_id] = KGNode(output_id, {
                            'primary_id': output_primary_id,
                            'qg_id': output_qg_id,
                            'equivalent_ids': self.helper._get_output_equivalent_ids(record),
                            'names': self.helper._get_output_names(record),
                            'label': self.helper._get_output_label(record),
                            'category': self.helper._get_output_category(record),
                            'node_attributes': self.helper._get_output_attributes(record)
                        })

                    if input_id not in self.nodes:
                        self.nodes[input_id] = KGNode(input_id, {
                            'primary_id': input_primary_id,
                            'qg_id': input_qg_id,
                            'equivalent_ids': self.helper._get_input_equivalent_ids(record),
                            'names': self.helper._get_input_names(record),
                            'label': self.helper._get_input_label(record),
                            'category': self.helper._get_input_category(record),
                            'node_attributes': self.helper._get_input_attributes(record)
                        })

                    self.nodes[output_id].add_source_node(input_id)
                    self.nodes[output_id].add_source_qg_node(input_qg_id)
                    self.nodes[input_id].add_target_node(output_id)
                    self.nodes[input_id].add_target_qg_node(output_qg_id)
                    if edge_id not in self.edges:
                        self.edges[edge_id] = KGEdge(edge_id, {
                            'predicate': self.helper._get_predicate(record),
                            'subject': input_primary_id,
                            'object': output_primary_id
                        })

                    self.edges[edge_id].add_api(self.helper._get_api(record))
                    self.edges[edge_id].add_source(self.helper._get_source(record))
                    self.edges[edge_id].add_publication(self.helper._get_publication(record))
                    for key in record:
                        if not (key in bte_attributes or key.startswith('$')):
                            self.edges[edge_id].add_additional_attributes(key, record[key])

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.subscribers = [fn for fn in self.subscribers if fn != subscriber]

    def notify(self):
        for subscriber in self.subscribers:
            subscriber.update({
                'nodes': self.nodes,
                'edges': self.edges,
            })
