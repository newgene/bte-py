import copy

from ..json_transform.index import transform
from ..utils import generate_curie, to_array


class BaseTransformer:
    edge = {}
    data = {}

    def __init__(self, data):
        self.data = data
        self.edge = data['edge']

    def pair_input_with_api_response(self):
        _input = generate_curie(self.edge['association']['input_id'], self.edge['input'])
        return {
            _input: [self.data['response']]
        }

    def wrap(self, res):
        if isinstance(res, list):
            res = {'data': res}
        return res

    def json_transform(self, res):
        res = transform(res, self.edge['response_mapping'])
        return res

    def _update_publications(self, res):
        if 'pubmed' in res:
            res['pubmed'] = to_array(res['pubmed'])
            res['publications'] = [item.upper() if isinstance(item, str) and item.upper().startswith('PMID:') else 'PMID:' + str(item) for item in res['pubmed']]
            res.pop('pubmed', None)
        if 'pmc' in res:
            res['pmc'] = to_array(res['pmc'])
            res['publications'] = [item.upper() if isinstance(item, str) and item.upper().startswith('PMC:') else 'PMC:' + str(item)
                                   for item in res['pmc']]
            res.pop('pmc', None)
        return res

    def _update_edge_metadata(self, res):
        res['$edge_metadata'] = {
            **self.edge['association'],
            'trapi_qEdge_obj': self.edge.get('reasoner_edge'),
            'filter': self.edge.get('filter')
        }
        return res

    def _update_input(self, res, _input):
        res['$input'] = {
            'original': None if not self.edge.get('original_input') else self.edge['original_input'][_input],
            'obj': None if not (self.edge.get('input_resolved_identifiers') and self.edge.get('original_input')) else self.edge['input_resolved_identifiers'][self.edge['original_input'][_input]]
        }
        return res

    def _remove_non_edge_data(self, res):
        res.pop('@type', None)
        res.pop(self.edge['association']['output_id'])
        return res

    def add_edge_info(self, _input, res):
        if not res or len(res) == 0:
            return []
        res = self._update_edge_metadata(res)
        res = self._update_input(res, _input)
        output_ids = self.extract_output_ids(res)
        result = []
        for item in output_ids:
            copy_res = copy.deepcopy(res)
            copy_res['$edge_metadata'] = res['$edge_metadata']
            copy_res['$output'] = {
                'original': item
            }

            copy_res = self._remove_non_edge_data(copy_res)
            copy_res = self._update_publications(copy_res)
            result.append(copy_res)
        return result

    def extract_output_ids(self, res):
        output_id_type = self.edge['association']['output_id']
        if output_id_type not in res:
            return []
        res[output_id_type] = to_array(res[output_id_type])
        return [generate_curie(output_id_type, item) for item in res[output_id_type]]

    def transform(self):
        result = []
        responses = self.pair_input_with_api_response()
        for curie in responses:
            if isinstance(responses[curie], list) and len(responses[curie]) > 0:
                for item in responses[curie]:
                    item = self.wrap(item)
                    item = self.json_transform(item)
                    for predicate in item:
                        if isinstance(item[predicate], list) and len(item[predicate]) > 0:
                            for rec in item[predicate]:
                                rec = self.add_edge_info(curie, rec)
                                result = [*result, *rec]
                        else:
                            result = [*result, *self.add_edge_info(curie, item[predicate])]
        return result
