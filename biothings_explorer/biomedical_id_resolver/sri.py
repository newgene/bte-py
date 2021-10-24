import requests
from urllib import parse
from .config import CURIE


def query(api_input):
    url = 'https://nodenormalization-sri-dev.renci.org/1.1/get_normalized_nodes'
    params = {'curie': [item for item in api_input]}
    search = parse.urlencode(params, True)
    if search:
        url = f"{url}?{search}"
    r = requests.get(url)
    data = r.json()
    return data


def transform_results(results):
    for key in results:
        entry = results[key]
        id_type = key.split(":")[0]
        if not entry:
            entry = {
                'id': {
                    'identifier': key,
                    'label': key,
                },
                'primaryID': key,
                'label': key,
                'curies': [key],
                'attributes': {},
                'semanticType': '',
                'semanticTypes': [''],
                'dbIDs': {
                    id_type: key if id_type in CURIE['ALWAYS_PREFIXED'] else key.split(':')[1]
                }
            }
        else:
            entry['primaryID'] = entry['id']['identifier']
            entry['label'] = entry['id']['label'] or entry['id']['identifier']
            entry['attributes'] = {}
            entry['semanticType'] = entry['type'][0].split(':')[1]
            entry['semanticTypes'] = entry['type']
            entry['curies'] = list(set([id_obj.get('identifier') for id_obj in entry['equivalent_identifiers'] if id_obj.get('identifier')]))
            entry['dbIDs'] = {}
            for id_obj in entry['equivalent_identifiers']:
                id_type = id_obj['identifier'].split(':')[0]
                if id_type in CURIE['ALWAYS_PREFIXED']:
                    if isinstance(entry['dbIDs'].get(id_type), list):
                        entry['dbIDs'][id_type].append(id_obj['identifier'])
                    else:
                        entry['dbIDs'][id_type] = [id_obj['identifier']]
                else:
                    curie_without_prefix = id_obj['identifier'].split(':')[1]
                    if isinstance(entry['dbIDs'].get(id_type), list):
                        entry['dbIDs'][id_type].append(curie_without_prefix)
                    else:
                        entry['dbIDs'][id_type] = [curie_without_prefix]
            entry['dbIDs']['name'] = list(set([id_obj.get('label') for id_obj in entry['equivalent_identifiers'] if id_obj.get('label')]))
        results[key] = [entry]
    return results
