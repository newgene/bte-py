import logging

logger = logging.getLogger(__name__)


def format_response(response_data, config):
    output = []
    subject_type = config["subject"]
    object_type = config["object"]
    predicate = config["predicate"]
    response_mapping = config["bte"]["response_mapping"][predicate]

    # Determining the fields for objects using response mapping and configuration
    object_fields = {key: value.split(".") for key, value in response_mapping.items()}

    item = response_data
    # Dynamically determine the subject ID field from config or infer from item keys
    subject_id_field = determine_subject_id_field(
        item, config["bte"]["query_operation"]["request_body"]["body"]["scopes"]
    )
    subject_id = item.get(subject_id_field, None)
    if not subject_id:
        logger.warning("Found no subject id")
        return []

    for field_name, path in object_fields.items():
        current_data = navigate_path(item, path)

        # Process multiple objects or a single object scenario
        if isinstance(current_data, list):
            for obj in current_data:
                if isinstance(obj, dict):
                    for sub_field in obj:
                        formatted_item = create_formatted_item(
                            subject_type,
                            subject_id_field,
                            subject_id,
                            object_type,
                            predicate,
                            sub_field,
                            obj[sub_field],
                        )
                        output.append(formatted_item)
                else:
                    formatted_item = create_formatted_item(
                        subject_type,
                        subject_id_field,
                        subject_id,
                        object_type,
                        predicate,
                        field_name,
                        obj,
                    )
                    output.append(formatted_item)
        elif current_data:
            formatted_item = create_formatted_item(
                subject_type,
                subject_id_field,
                subject_id,
                object_type,
                predicate,
                field_name,
                current_data,
            )
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
    current_data = data
    for part in path:
        if isinstance(current_data, dict) and part in current_data:
            current_data = current_data[part]
        elif isinstance(current_data, list):
            current_data = [obj.get(part) for obj in current_data if part in obj]
        else:
            return
    return current_data


def create_formatted_item(
    subject_type,
    subject_id_field,
    subject_id,
    object_type,
    predicate,
    field_name,
    object_id,
):
    """Helper function to create a formatted dictionary item"""
    return {
        "subject": {"type": subject_type, subject_id_field: subject_id},
        "predicate": predicate,
        "object": {"type": object_type, field_name: object_id},
    }
