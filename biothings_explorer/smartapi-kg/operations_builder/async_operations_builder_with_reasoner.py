import requests
from .async_operations_builder import AsyncOperationsBuilder
from ..parser.index import API


class AsyncOperationsBuilderWithReasoner(AsyncOperationsBuilder):

    def get_TRAPI_with_predicates_endpoint(self, specs):
        trapi = []
        for spec in specs:
            try:
                parser = API(spec)
                metadata = parser.metadata
                if "/predicates" in metadata.paths and "/query" in metadata.paths and metadata["x-translator"].team:
                    trapi.append(metadata)
            except Exception as e:
                pass
        return trapi

    def construct_query_url(self, server_url):
        if server_url.endswith('/'):
            server_url = server_url[:-1]
        return server_url + "/predicates"

    def remove_bio_link_prefix(self, _input):
        if not isinstance(_input, str):
            return None
        if _input.startswith('biolink:'):
            return _input[8:]
        return _input

    def parse_predicate_endpoint(self, response, metadata):
        ops = []
        for sbj in response:
            for obj in response[sbj]:
                if isinstance(response[sbj][obj], list):
                    for pred in response[sbj][obj]:
                        ops.append({
                            'association':{
                                'input_type': self.remove_bio_link_prefix(sbj),
                                'output_type': self.remove_bio_link_prefix(obj),
                                'predicate': self.remove_bio_link_prefix(pred),
                                'api_name': metadata.title,
                                'smartapi': metadata.smartapi,
                                'x-translator': metadata['x-translator'],
                            },
                            'tags': [*metadata.tags, 'bte-trapi'],
                            'query_operation': {
                                'path': '/query',
                                'method': 'post',
                                'server': metadata.url,
                                'path_params': None,
                                'params': None,
                                'request_body': None,
                                'support_batch': True,
                                'input_separator': ',',
                                'tags': [*metadata.tags, 'bte-trapi']
                            }
                        })
        return ops

    def get_ops_from_predicates_endpoint(self, metadata):
        response = requests.get(self.construct_query_url(metadata.url))
        if response.status_code == 200:
            data = response.json()
            return self.parse_predicate_endpoint(data)
        return []

    def get_ops_from_predicates_endpoints(self, specs):
        metadatas = self.get_TRAPI_with_predicates_endpoint(specs)
        res = []
        for metadata in metadatas:
            response = self.get_ops_from_predicates_endpoint(metadata)
            for ops in response.value:
                res = [*res, *response.value]
        return res

    def build(self):
        specs = self.load()
        non_TRAPI_ops = self.load_ops_from_specs(specs)
        TRAPI_ops = self.get_ops_from_predicates_endpoints(specs)
        return [*non_TRAPI_ops, *TRAPI_ops]
