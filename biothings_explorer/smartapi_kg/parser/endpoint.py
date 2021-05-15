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
        if "parameters" not in operation_object:
            return params
        for param in operation_object['parameters']:
            if param['in'] == 'path':
                params.append(param['name'])
        return params

    def construct_query_operation(self, data):
        op, method, path_params = itemgetter('op', 'method', 'path_params')(data)
        server = self.api_meta_data['url']
        query_operation = QueryOperationObject()
        query_operation.xBTEKGSOperation = op
        query_operation.method = method
        query_operation.path_params = path_params
        query_operation.server = server
        query_operation.path = self.path
        query_operation.tags = self.api_meta_data['tags']
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

    def construct_response_mapping(self, op):
        if "response_mapping" in op:
            op.response_mapping = op.response_mapping

        return {
            f"{op.predicate}": self.resolve_ref_if_provided(op.response_mapping)
        }

    def parse_individual_operation(self, op, method, path_params):
        res = []
        query_operation = self.construct_query_operation({'op': op, 'method': method, 'path_params': path_params})
        response_mapping = self.construct_response_mapping(op)
        for input in op.inputs:
            for output in op.outputs:
                update_info = {}
                association = self.construct_association(input, output, op)
                update_info = {
                    'query_operation': query_operation,
                    'association': association,
                    'response_mapping': response_mapping,
                    'tags': query_operation['tags']
                }
                res.append(update_info)
        return res

    def construct_endpoint_info(self):
        res = []
        for method in ['get', 'post']:
            if method in self.path_item_object:
                path_params = self.fetch_path_params(self.path_item_object[method])
                if "x-bte-kgs-operations" in self.path_item_object[method]:
                    for rec in self.path_item_object[method]['x-bte-kgs-operations']:
                        operation = self.resolve_ref_if_provided(rec)
                        operation = operation if isinstance(operation, list) else [operation]
                        for op in operation:
                            res = [
                                *res,
                                *self.parse_individual_operation(op, method, path_params)
                            ]
        return res
