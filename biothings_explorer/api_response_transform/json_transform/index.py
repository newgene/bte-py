from utils import separate_simple_an_complex_paths, transform_simple_object, transform_complex_object


def transform(json_doc, template):
    data = separate_simple_an_complex_paths(template)
    simple_path_template = data.get("simple_path_template")
    complex_path_template = data.get("complex_path_template")
    transformed_json_doc = transform_simple_object(json_doc, simple_path_template)
    for key, value in complex_path_template.items():
        if isinstance(value, list):
            transformed_json_doc[key] = [transform_complex_object(json_doc, tmpl) for tmpl in value]
        else:
            transformed_json_doc[key] = transform_complex_object(json_doc, value)
    return transformed_json_doc
