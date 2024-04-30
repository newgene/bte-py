import logging

logger = logging.getLogger(__name__)


def format_response(response_data, config):
    output = []
    subject_type = config["subject"]
    object_type = config["object"]
    predicate_type = config["predicate"]
    response_mapping = config["bte"]["response_mapping"][predicate_type]

    if isinstance(response_data, dict):
        response_data = [response_data]

    for item in response_data:
        # Fetch subject ID based on the provided 'scopes' or fallback to '_id'
        subject_field = determine_subject_id_field(
            item, config["bte"]["query_operation"]["request_body"]["body"]["scopes"]
        )
        subject_id = item.get(subject_field, item.get("_id"))

        # Initialize object info with keys from response_mapping, default to None if not present
        object_info = {
            key: navigate_path(item, value.split("."))
            for key, value in response_mapping.items()
        }

        # Format the complete item
        formatted_item = {
            "subject": {"type": subject_type, subject_field: subject_id},
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
