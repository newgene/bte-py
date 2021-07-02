import os
import requests
import json
import schedule
import time


def get_trapi_with_predicates_endpoint(specs):
    trapi = []
    special_cases = []
    for spec in specs:
        if 'info' in spec and 'x-translator' in spec['info'] and spec['info']['x-translator']['component'] == 'KP' and \
                'paths' in spec and '/query' in spec['paths'] and 'x-trapi' in spec['info'] and len(spec['servers']) and \
                '/predicates' in spec['paths'] or '/meta_knowledge_graph' in spec[
            'paths'] or '/1.1/meta_knowledge_graph' \
                in spec['paths']:
            api = {
                'association': {
                    'api_name': spec['info']['title'],
                    'smartapi': {
                        'id': spec['_id'],
                        'meta': spec['_meta']
                    },
                    'x-translator': {
                        'component': 'KP',
                        'team': spec['info']['x-translator']['team']
                    }
                },
                'tags': [item.name for item in spec['tags']],
                'query_operation': {
                    'path': '/query',
                    'server': spec['servers'][0]['url'],
                    'method': 'post'
                }
            }
            if '/meta_knowledge_graph' in spec['paths'] and 'version' in spec['info']['x-trapi'] and \
                '1.1' in spec['info']['x-trapi']['version']:
                # 1.1
                api['predicates_path'] = '/meta_knowledge_graph'
                trapi.append(api)
            if '/1.1/meta_knowledge_graph' in spec['paths'] and 'version' in spec['info']['x-trapi'] and \
                    '1.1' in spec['info']['x-trapi']['version']:
                # 1.1
                api['predicates_path'] = '/1.1/meta_knowledge_graph'
                trapi.append(api)
                special_cases.append({'name': spec['info']['title'], 'id': spec['_id']})
            elif '/predicates' in spec['paths']:
                # 1.0
                api['predicates_path'] = '/predicates'
                trapi.append(api)
            else:
                pass
    return trapi


def construct_query_url(server_url, path):
    if server_url.endswith('/'):
        server_url = server_url[0:-1]
    return server_url + path


def get_predicates_from_graph_data(predicate_endpoint, data):
    if predicate_endpoint not in ['/meta_knowledge_graph', '/1.1/meta_knowledge_graph']:
        return data
    predicates = {}

    def add_new_predicates(edge):
        if edge['object'] in predicates:
            predicates[edge['object']][edge['subject']] = edge['predicate']
        else:
            predicates[edge['object']] = {}
            predicates[edge['object']][edge['subject']] = edge['predicate']

    if 'edges' in data:
        for edge in data['edges']:
            add_new_predicates(edge)
    else:
        return data

    return predicates


def get_ops_from_endpoint(metadata):
    url = construct_query_url(metadata['query_operation']['server'], metadata['predicates_path'])
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            **metadata,
            'predicates': get_predicates_from_graph_data(metadata['predicates_path'], data)
        }
    return False


def get_ops_from_predicates_endpoints(specs):
    metadatas = get_trapi_with_predicates_endpoint(specs)
    res = []
    results = []
    for metadata in metadatas:
        result = get_ops_from_endpoint(metadata)
        results.append(result)

    for rec in results:
        if rec:
            res.append(rec)
    return res


def update_smart_api_specs():
    SMARTAPI_URL = 'https://smart-api.info/api/query?q=tags.name:translator&size=150&fields=paths,servers,tags,components.x-bte*,info,_meta'
    res = requests.get(SMARTAPI_URL)
    data = res.json()
    local_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'smartapi_specs.json'))

    predicates_file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'predicates.json'))

    with open(local_file_path, mode='write') as f:
        f.write(json.dumps(data))

    predicates_info = get_ops_from_predicates_endpoints(data['hits'])
    with open(predicates_file_path, mode='write') as f:
        f.write(json.dumps(predicates_info))


def job():
    update_smart_api_specs()


def update_scheduler():
    schedule.every(10).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
