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
        for record in query_result:
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
                    'label': self.helper._get_output_label(record),
                    'category': self.helper._get_output_category(record),
                    'node_attributes': self.helper._get_output_attributes(record)
                })

            if input_id not in self.nodes:
                self.nodes[input_id] = KGNode(input_id, {
                    'primary_id': input_primary_id,
                    'qg_id': input_qg_id,
                    'equivalent_ids': self.helper._get_input_equivalent_ids(record),
                    'label': self.helper._get_input_label(record),
                    'category': self.helper._get_input_category(record),
                    'node_attributes': self.helper._get_input_attributes(record)
                })
