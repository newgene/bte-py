import requests
import functools
import copy
from urllib import parse
from .config import CURIE


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def combine_inputs(user_input):
    reduced = functools.reduce(
        lambda prev, current: [*prev, *user_input[current]], user_input, [])
    return list(set(reduced))


def query(api_input):
    url = 'https://nodenormalization-sri.renci.org/1.2/get_normalized_nodes'
    # chunks of 1500 continuously throw 414 unlike the js version
    chunked_input = chunks(api_input, 100)
    queries = []
    for _input in chunked_input:
        params = {'curie': [item for item in _input]}
        search = parse.urlencode(params, True)
        if search:
            url = f"{url}?{search}"

        r = requests.get(url)
        # Sometimes throws 502
        try:
            data = r.json()
            queries.append(data)
        except Exception as e:
            pass
    result = {}
    for outer_key, _query in enumerate(queries):
        for key, value in enumerate(_query):
            result[value] = _query[value]
    return result


def unresolvable_entry(curie, semantic_type):
    id_type = curie.split(':')[0]
    return{
        'id':{
            'identifier': curie,
            'label': curie
        },
        'equivalent_identifiers': [{
            'identifier': curie,
            'label': curie
        }],
        'primaryID': curie,
        'label': curie,
        'curies': [curie],
        'attributes': {},
        'semanticType': semantic_type,
        '_leafSemanticType': semantic_type,
        'type': [semantic_type],
        'semanticTypes': [semantic_type],
        'dbIDs': {
            id_type: [curie if id_type in CURIE['ALWAYS_PREFIXED'] else curie.split(':')[1]],
            'name': [curie]
        },
        '_dbIDs': {
            id_type: [curie if id_type in CURIE['ALWAYS_PREFIXED'] else curie.split(':')[1]],
            'name': [curie]
        }
    }


def resolvable_entity(sri_entry):
    entry = sri_entry

    entry['primaryID'] = entry['id']['identifier']
    entry['label'] = entry['id'].get('label') or entry['id']['identifier']
    entry['attributes'] = {}
    entry['semanticType'] = entry['type'][0].split(':')[1]
    entry['_leafSemanticType'] = entry['semanticType']
    entry['semanticTypes'] = entry['type']

    names = list(set([id_obj.get('label') for id_obj in entry['equivalent_identifiers'] if id_obj.get('label')]))
    curies = list(set([id_obj.get('identifier') for id_obj in entry['equivalent_identifiers'] if id_obj.get('identifier')]))
    entry['curies'] = [*curies]
    entry['dbIDs'] = {}

    for id_obj in entry['equivalent_identifiers']:
        id_type = id_obj['identifier'].split(':')[0]
        if not isinstance(entry['dbIDs'].get(id_type), list):
            entry['dbIDs'][id_type] = []

        if id_type in CURIE['ALWAYS_PREFIXED']:
            entry['dbIDs'][id_type].append(id_obj['identifier'])
        else:
            curie_without_prefix = id_obj['identifier'].split(':')[1]
            entry['dbIDs'][id_type].append(curie_without_prefix)
    entry['dbIDs']['name'] = names
    entry['_dbIDs'] = entry['dbIDs']

    return entry


def transform_results(results):
    for key in results:
        entry = results[key]
        if not entry:
            entry = unresolvable_entry(key, None)
        else:
            entry = resolvable_entity(entry)
        results[key] = [entry]
    return results


def map_input_semantic_types(original_input, result):
    for semantic_type in original_input:
        if semantic_type == 'unknown' or semantic_type == 'NamedThing' or not semantic_type:
            continue
        unique_inputs = list(set(original_input[semantic_type]))
        for curie in unique_inputs:
            entry = result[curie][0]
            if not entry['semanticType']:
                entry['_leafSemanticType'] = semantic_type
                entry['semanticType'] = semantic_type
                entry['semanticTypes'] = [semantic_type]
                entry['type'] = [semantic_type]
            elif entry['semanticType'] != semantic_type:
                new_entry = copy.deepcopy(entry)
                new_entry['_leafSemanticType'] = semantic_type
                new_entry['semanticType'] = semantic_type
                new_entry['semanticTypes'][0] = semantic_type
                new_entry['type'][0] = semantic_type
                result[curie].append(new_entry)
    return result


def _resolve_sri(user_input):
    unique_input_ids = combine_inputs(user_input)
    query_results = query(unique_input_ids)
    query_results = transform_results(query_results)
    query_results = map_input_semantic_types(user_input, query_results)
    return query_results
