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
            'categories': ['biolink:' + kg_node._semantic_type],
            'name': kg_node._label,
            'attributes': [
                {
                    'attribute_type_id': 'biolink:xref',
                    'value': kg_node._curies,
                },
                {
                    'attribute_type_id': 'biolink:synonym',
                    'value': kg_node._names,
                },
                {
                    'attribute_type_id': 'num_source_nodes',
                    'value': len(kg_node._source_nodes),
                },
                {
                    'attribute_type_id': 'num_target_nodes',
                    'value': len(kg_node._target_nodes),
                },
                {
                    'attribute_type_id': 'source_qg_nodes',
                    'value': [item for item in kg_node._source_qg_nodes],
                },
                {
                    'attribute_type_id': 'target_qg_nodes',
                    'value': [item for item in kg_node._target_qg_nodes],
                },
            ]
        }
        for key in kg_node._node_attributes:
            res['attributes'].append({
                'attribute_type_id': key,
                'value': kg_node._node_attributes[key],
            })
        return res

    def _create_attributes(self, kg_edge):
        attributes = [
            {
                'attribute_type_id': 'biolink:aggregator_knowledge_source',
                'value': ['infores:translator-biothings-explorer'],
                'value_type_id': 'biolink:InformationResource'
            },
        ]
        items = [
            'Clinical Risk KP API',
            'Text Mining Targeted Association API',
            'Multiomics Wellness KP API',
            'Drug Response KP API',
            'Text Mining Co-occurrence API',
            'TCGA Mutation Frequency API',
          ]
        if kg_edge['attributes'].get('edge-attributes'):
            attributes = [*attributes, *kg_edge['attributes']['edge-attributes']]
        elif any(api_name for api_name in items if api_name in kg_edge['apis']):
            attributes = [*attributes]
            if len(list(kg_edge['sources'])):
                attributes = [
                    *attributes,
                    {
                        'attribute_type_id': 'biolink:primary_knowledge_source',
                        'value': list(kg_edge['sources']),
                        'value_type_id': 'biolink:InformationResource'
                    }
                ]
            if len(list(kg_edge['infores_curies'])):
                attributes = [
                    *attributes,
                    {
                        'attribute_type_id': 'biolink:primary_knowledge_source',
                        'value': list(kg_edge['infores_curies']),
                        'value_type_id': 'biolink:InformationResource'
                    }
                ]
            if len(list(kg_edge['publications'])):
                attributes = [
                    *attributes,
                    {
                        'attribute_type_id': 'biolink:publications',
                        'value': list(kg_edge['publications']),
                    }
                ]
            for key in kg_edge['attributes']:
                attributes.append({
                    'attribute_type_id': key,
                    'value': kg_edge['attributes'][key]
                })
        else:
            attributes = [*attributes]
            if len(list(kg_edge['sources'])):
                attributes = [
                    *attributes,
                    {
                        'attribute_type_id': 'biolink:primary_knowledge_source',
                        'value': list(kg_edge['sources']),
                        'value_type_id': 'biolink:InformationResource'
                    }
                ]
            if len(list(kg_edge['infores_curies'])):
                attributes = [
                    *attributes,
                    {
                        'attribute_type_id': 'biolink:aggregator_knowledge_source',
                        'value': list(kg_edge['infores_curies']),
                        'value_type_id': 'biolink:InformationResource'
                    }
                ]
            if len(list(kg_edge['publications'])):
                attributes = [
                    *attributes,
                    {
                        'attribute_type_id': 'biolink:publications',
                        'value': list(kg_edge['publications']),
                    }
                ]
            for key in kg_edge['attributes']:
                attributes.append({
                    'attribute_type_id': key,
                    'value': kg_edge['attributes'][key]
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
        for node in bte_graph['nodes']:
            self.nodes[bte_graph['nodes'][node]._primary_id] = self._create_node(bte_graph['nodes'][node])
        for edge in bte_graph['edges']:
            self.edges[edge] = self._create_edge(bte_graph['edges'][edge])
        self.kg = {
            'nodes': self.nodes,
            'edges': self.edges,
        }
