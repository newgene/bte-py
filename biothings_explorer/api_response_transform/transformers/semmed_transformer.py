from biothings_transformer import BioThingsTransformer


class SemmedTransformer(BioThingsTransformer):
    def wrap(self, res):
        result = {}
        for predicate in res:
            tmp = []
            if isinstance(res['predicate'], list) and len(res['predicate']) > 0:
                for item in res['predicate']:
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
