
from biothings_explorer.api_response_transform.json_transform.index import transform
from biothings_explorer.api_response_transform.transformers.biothings_transformer import (
    BioThingsTransformer,
)
from biothings_explorer.api_response_transform.utils import generate_curie

from .edge import MetaKGEdge


class BioThingsTransformer_v2(BioThingsTransformer):
    def json_transform(self, res):
        res = transform(res, self.edge.response_mapping)
        return res

    def pair_input_with_api_response(self):
        if self.edge.query_operation.method == 'post':
            res = {}
            for item in self.data['response']:
                if 'notfound' not in item:
                    _input = generate_curie(self.edge.subject_prefix, item['query'])
                    if _input in res:
                        res[_input].append(item)
                    else:
                        res[_input] = [item]
            return res
        else:
            _input = generate_curie(self.edge.subject_prefix, self.edge['input'])
            return {_input: [self.data['response']]}

    def add_edge_info(self, subject_id, object_info):
        formatted_edge = {
            "subject": {"type": self.edge.subject, "id": subject_id},
            "predicate": {"type": self.edge.predicate},
            "object": {"type": self.edge.object, **object_info},
        }
        object_prefix = self.edge.object_prefix
        if object_prefix and object_prefix in object_info:
            object_id = generate_curie(object_prefix, object_info[object_prefix])
            formatted_edge["object"]["id"] = object_id
        return formatted_edge

    def transform(self):
        result = []
        responses = self.pair_input_with_api_response()
        for curie in responses:
            if isinstance(responses[curie], list) and len(responses[curie]) > 0:
                for item in responses[curie]:
                    item = self.wrap(item)
                    item = self.json_transform(item)
                    for predicate in item:
                        if isinstance(item[predicate], list) and len(item[predicate]) > 0:
                            # for rec in item[predicate]:
                            #     rec = self.add_edge_info(curie, rec)
                            #     result = [*result, *rec]
                            result.extend([self.add_edge_info(curie, rec) for rec in item[predicate] if rec])
                        else:
                            # result = [*result, *self.add_edge_info(curie, item[predicate])]
                            if item[predicate]:
                                result.append(self.add_edge_info(curie, item[predicate]))
        return result


def format_response_v2(response_data, edge: MetaKGEdge):
    tf_obj = BioThingsTransformer_v2({'response': response_data, 'edge': edge})
    # TODO
    # data can sometimes have values like 'msg': 'field required' instead of actual data
    # if this is the case the below function returns None
    transformed = tf_obj.transform()
    return transformed


def format_response(response_data, edge: MetaKGEdge):
    output = []
    subject_type = edge.subject
    subject_prefix = edge.subject_prefix
    object_type = edge.object
    object_prefix = edge.object_prefix
    predicate_type = edge.predicate
    response_mapping = edge.response_mapping[predicate_type]

    if isinstance(response_data, dict):
        response_data = [response_data]

    for item in response_data:
        # Initialize object info with keys from response_mapping, default to None if not present
        object_id = item.pop("_id")
        if object_id and object_prefix:
            object_id = f"{object_prefix}:{object_id}"
        object_info = {
            key: navigate_path(item, value.split("."))
            for key, value in response_mapping.items()
        }

        # Format the complete item
        subject_id = item["query"]
        if subject_prefix:
            subject_id = f"{subject_prefix}:{item['query']}"

        formatted_item = {
            "subject": {"type": subject_type, "id": subject_id},
            "predicate": {"type": predicate_type},
            "object": {"type": object_type, "id": object_id, **object_info},
        }
        output.append(formatted_item)

    return output


def determine_subject_id_field(item, scope):
    """Dynamically determine the subject ID field from configuration scope or guess from item keys"""
    if isinstance(item, str):
        if item == scope:
            return scope
    else:
        if scope in item:
            return scope
        # As a fallback, guess the subject ID from the first likely identifier key
        return next((k for k in item.keys() if "id" in k.lower()), None)


def navigate_path(data, path):
    """Navigate through the nested structures based on the path"""
    for part in path:
        if isinstance(data, dict) and part in data:
            data = data[part]
        else:
            return
    return data
