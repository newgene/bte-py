from .transformer import BaseTransformer


class OpenTargetTransformer(BaseTransformer):
    def wrap(self, res):
        tmp = []
        for item in res['data']:
            if 'drug' in item and 'id' in item['drug'] and isinstance(item['drug']['id'], str) and 'CHEMBL' in item['drug']['id']:
                item['drug']['id'] = item['drug']['id'].split('/')[-1]
            tmp.append(item)
        res['data'] = tmp
        return res
