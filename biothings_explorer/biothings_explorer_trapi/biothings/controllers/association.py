import os
from biothings_explorer.smartapi_kg.metakg import MetaKG


def association(sub=None, obj=None, pred=None, api=None, source=None):
    smartapi_specs = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'smartapi_specs.json'))

    predicates = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'predicates.json'))

    kg = MetaKG(smartapi_specs, predicates)
    kg.construct_MetaKG_sync(True, {})
    associations = []
    filtered_res = kg.filter({
        'input_type': sub,
        'output_type': obj,
        'predicate': pred,
        'api_name': api,
        'source': source
    })
    for op in filtered_res:
        associations.append({
            'subject': op['association']['input_type'],
            'object': op['association']['output_type'],
            'predicate': op['association']['predicate'],
            'provided_by': op['association']['source'],
            'api': {
                'name': op['association']['api_name'],
                'smartapi': {
                    'metadata': op['association']['smartapi']['meta']['url'],
                    'id': op['association']['smartapi']['id'],
                    'ui': "https://smart-api.info/ui/" + op['association']['smartapi']['id']
                },
                'x-translator': op['association']['x-translator']
            }
        })
    return associations
