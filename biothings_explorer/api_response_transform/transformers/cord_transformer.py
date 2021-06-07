from .biothings_transformer import BioThingsTransformer


class CordTransformer(BioThingsTransformer):
    def wrap(self, res):
        PREFIXES = ['pr', 'go', 'mop', 'hgnc', 'uberon', 'so', 'cl', 'doid', 'chebi']
        result = {}
        for predicate in res:
            tmp = []
            if isinstance(res[predicate], list) and len(res[predicate]) > 0:
                for item in res[predicate]:
                    if item['@type'] == self.edge['association']['output_type'] or \
                            (item['@type'] == 'DiseaseOrPhenotypicFeature' and
                             self.edge['association']['output_type'] == 'Disease'):
                        for key in list(item):
                            if key in PREFIXES:
                                item[key.upper()] = item[key]
                                item.pop(key, None)
                        tmp.append(item)
            if len(tmp) > 0:
                result['related_to'] = tmp
        return result

    def json_transform(self, res):
        return res
