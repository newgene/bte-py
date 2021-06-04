from transformer import BaseTransformer
from ..utils import generate_curie


class BioThingsTransformer(BaseTransformer):
    def pair_input_with_api_response(self):
        if self.edge['query_operation']['method'] == 'post':
            res = {}
            for item in self.data['response']:
                if 'notfound' not in item:
                    _input = generate_curie(self.edge['association']['input_id'], item['query'])
                    if _input in res:
                        res[_input].append(item)
                    else:
                        res[_input] = [item]
            return res
        else:
            _input = generate_curie(self.edge['association']['input_id'], self.edge['input'])
            return {[_input]: [self.data['response']]}
