import logging

from .edge import MetaKGEdge

logger = logging.getLogger(__name__)


def format_response(response_data, edge: MetaKGEdge):
    output = []
    subject_type = edge.subject
    object_type = edge.object
    predicate_type = edge.predicate
    response_mapping = edge.response_mapping[predicate_type]

    if isinstance(response_data, dict):
        response_data = [response_data]

    for item in response_data:
        # Initialize object info with keys from response_mapping, default to None if not present
        object_info = {
            key: navigate_path(item, value.split("."))
            for key, value in response_mapping.items()
        }

        # Format the complete item
        formatted_item = {
            "subject": {"type": subject_type, "_id": item["query"]},
            "predicate": {"type": predicate_type},
            "object": {"type": object_type, **object_info},
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
