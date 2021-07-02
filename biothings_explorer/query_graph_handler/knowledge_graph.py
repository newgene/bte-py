from .helper import QueryGraphHelper
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

    def _create_input_node(self, record):
        res = {
            'categories': 'biolink:' + helper._get_input_category(record),
            'name': helper._get_input_label(record),
            'attributes': [
                {
                    'name': 'equivalent_identifiers',
                    'value': helper._get_input_equivalent_ids(record),
                    'type': 'biolink:id'
                }
            ]
        }
        additional_attributes = helper._get_input_attributes(record)
        if additional_attributes:
            for key in additional_attributes:
                res['attributes'].append({
                    'name': key,
                    'value': additional_attributes[key],
                    'type': 'bts:' + key,
                })
        return res

    def _create_output_node(self, record):
        res = {
            'categories': 'biolink:' + helper._get_output_category(record),
            'name': helper._get_output_label(record),
            'attributes': [
                {
                    'name': 'equivalent_identifiers',
                    'value': helper._get_output_equivalent_ids(record),
                    'type': 'biolink:id'
                }
            ]
        }
        additional_attributes = helper._get_output_attributes(record)
        if additional_attributes:
            for key in additional_attributes:
                res['attributes'].append({
                    'name': key,
                    'value': additional_attributes[key],
                    'type': 'bts:' + key,
                })
        return res

    def _create_attributes(self, record):
        bte_attributes = ['name', 'label', 'id', 'api', 'provided_by']
        attributes = [
            {
                'name': 'provided_by',
                'value': helper._get_source(record),
                'type': 'biolink:provided_by'
            },
            {
                'name': 'api',
                'value': helper._get_api(record),
                'type': 'bts:api',
            }
        ]
        for key in record:
            if not (key in bte_attributes or key.startswith('$')):
                attributes.append({
                    'name': key,
                    'value': record[key],
                    'type': 'biolink:' + key if key == 'publications' else 'bts:' + key
                })
        return attributes

    def _create_edge(self, record):
        return {
            'predicate': helper._get_predicate(record),
            'subject': helper._get_input_id(record),
            'object': helper._get_output_id(record),
            'attributes': self._create_attributes(record),
        }

    def update(self, query_result):
        for record in query_result:
            if helper._get_input_id(record) not in self.nodes:
                self.nodes[helper._get_input_id(record)] = self._create_input_node(record)
            if helper._get_output_id(record) not in self.nodes:
                self.nodes[helper._get_output_id(record)] = self._create_output_node(record)
            if helper._create_unique_edge_id(record) not in self.edges:
                self.edges[helper._create_unique_edge_id(record)] = self._create_edge(record)
        self.kg = {
            'nodes': self.nodes,
            'edges': self.edges,
        }
