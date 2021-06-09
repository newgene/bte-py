from .transformer import BaseTransformer


class TRAPITransformer(BaseTransformer):
    def _get_unique_edges(self):
        edges = {}
        if 'messages' in self.data['responses'] and 'results' in self.data['response']['message'] and isinstance(self.data['response']['message']['results'], list):
            for item in self.data['response']['message']['results']:
                edges[item['edge_bindings']['e01'][0]['id']] = {
                    'subject': item['node_bindings']['n0'][0]['id'],
                    'object': item['node_bindings']['n1'][0]['id']
                }
        return edges

    def _get_edge_info(self, edge_id):
        if 'message' in self.data['response'] and 'knowledge_graph' in self.data['response']['message'] and 'edges' in self.data['response']['message']['knowledge_graph']:
            return self.data['response']['message']['knowledge_graph']['edges'][edge_id]
        return None

    def _transform_individual_edge(self, edge, edge_binding):
        res = {
            '$output': {
                'original': edge_binding['object']
            }
        }

        if 'attributes' in edge and isinstance(edge['attributes'], list):
            for attr in edge['attributes']:
                if 'name' in attr and 'value' in attr:
                    if attr['name'] not in ['subject', 'object']:
                        res[attr['name']] = attr['value']
            res = self._update_edge_metadata(res)
            res = self._update_input(res, edge_binding['subject'])
            return res

    def transform(self):
        edge_bindings = self._get_unique_edges()
        tmp = []
        for edge in edge_bindings:
            edge_info = self._get_edge_info(edge)
            if edge_info:
                return self._transform_individual_edge(edge_info, edge_bindings[edge])
