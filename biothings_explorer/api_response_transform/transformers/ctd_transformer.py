from transformer import BaseTransformer


class CTDTransformer(BaseTransformer):
    def wrap(self, res):
        tmp = []
        for item in res:
            if isinstance(item['PubMedIDs'], str):
                item['PubMedIDs'] = item['PubMedIDs'].split('|')
            if isinstance(item['DiseaseID'], str):
                item['DiseaseID'] = item['DiseaseID'].split(':')[-1]
            tmp.append(item)
        res = tmp
        return {'data': res}
