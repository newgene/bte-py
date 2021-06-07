from .transformer import BaseTransformer


class CTDTransformer(BaseTransformer):
    def wrap(self, res):
        tmp = []
        for item in res:
            if isinstance(item.get('PubMedIDs'), str):
                item['PubMedIDs'] = item['PubMedIDs'].split('|')
            if isinstance(item.get('DiseaseID'), str):
                item['DiseaseID'] = item['DiseaseID'].split(':')[-1]
            tmp.append(item)
        res = tmp
        return {'data': res}
