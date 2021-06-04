from transformer import BaseTransformer


class BiolinkTransformer(BaseTransformer):
    def wrap(self, res):
        PREFIXES = ['HGNC', 'NCBIGene', 'REACT']
        if 'association' in res:
            for rec in res['association']:
                if rec['object'] and 'id' in rec['object']:
                    [prefix, value] = rec['object']['id'].split(':')
                    if prefix in PREFIXES:
                        rec['object'][prefix] = value
                    else:
                        rec['object'][prefix] = rec['object']['id']
                if not rec['publications'] or len(rec['publications']) == 0 or not rec['publications'][0]['id'].startswith('PMID'):
                    rec.pop('publications', None)
                else:
                    rec['publications'] = [{'id': pub['id'].split(':')[-1]} for pub in rec['publications']]
                if 'provided_by' not in rec:
                    rec.pop('provided_by', None)
        return res
