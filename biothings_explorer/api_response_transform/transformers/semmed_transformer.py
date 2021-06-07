from .biothings_transformer import BioThingsTransformer


class SemmedTransformer(BioThingsTransformer):
    def wrap(self, res):
        result = {}
        for predicate in res:
            tmp = []
            if isinstance(res.get(predicate), list) and len(res.get(predicate)) > 0:
                for item in res.get(predicate):
                    if item['@type'] == self.edge['association']['output_type'] or \
                            (item['@type'] == 'DiseaseOrPhenotypicFeature' and self.edge['association']['output_type'] == 'Disease'):
                        item['UMLS'] = item['umls']
                        item['pubmed'] = item['pmid']
                        item.pop('umls', None)
                        item.pop('pmid', None)
                        tmp.append(item)
            if len(tmp) > 0:
                result[predicate] = tmp
        return result

    def json_transform(self, res):
        return res
