import re
from operator import itemgetter
from .query_operation import QueryOperationObject


class Endpoint:
    path_item_object = {}
    api_meta_data = {}
    path = ''

    def __init__(self, path_item_object, api_meta_data, path):
        self.path_item_object = path_item_object
        self.api_meta_data = api_meta_data
        self.path = path

    def fetch_path_params(self, operation_object):
        params = []
        if not "parameters" in operation_object:
            return params
        for param in operation_object.parameters:
            if param['in'] == 'path':
                params.append(param['name'])
        return params

    def construct_query_operation(self, data):
        op, method, path_params = itemgetter('op', 'method', 'path_params')(data)
        server = self.api_meta_data.url
        query_operation = QueryOperationObject()
        query_operation.xBTEKGSOperation = op
        query_operation.method = method
        query_operation.path_params = path_params
        query_operation.server = server
        query_operation.path = self.path
        query_operation.tags = self.api_meta_data.tags
        return query_operation

    def remove_bio_link_prefix(self, input):
        if not input:
            return input
        if input.startswith('biolink:'):
            return re.sub(r'/biolink:/gi', "", input)
        return input

    def resolve_ref_if_provided(self, rec):
        if "$ref" in rec:
            return self.api_meta_data.components.fetch_component_by_ref(rec['$ref'])
        return rec

    def construct_association(self, input, output, op):
        return {
            'input_id': self.remove_bio_link_prefix(input.id),
            'input_type': self.remove_bio_link_prefix(input.semantic),
            'output_id': self.remove_bio_link_prefix(output.id),
            'output_type': self.remove_bio_link_prefix(output.semantic),
            'predicate': self.remove_bio_link_prefix(op.predicate),
            'source': op.source,
            'api_name': self.api_meta_data.title,
            'smartapi': self.api_meta_data.smartapi,
            'x-translator': self.api_meta_data['x-translator']
        }
