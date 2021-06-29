import os
from jsonpath_ng import jsonpath, parse


def commonprefix(l, sep=os.sep):
    # this unlike the os.path.commonprefix version
    # always returns path prefixes as it compares
    # path component wise
    cp = []
    ls = [p.split(sep) for p in l]
    ml = min(len(p) for p in ls)

    for i in range(ml):

        s = set(p[i] for p in ls)
        if len(s) != 1:
            break

        cp.append(s.pop())

    return sep.join([*cp, ''])


def extract_paths_from_template(template):
    paths = []
    for value in template.values():
        if isinstance(value, str):
            paths.append(value)
        else:
            paths = [*paths, *value]
    return paths


def find_longest_common_path(paths):
    if len(paths) == 0:
        return None
    if len(paths) == 1:
        return paths[0]
    common_path = commonprefix(paths, '.')
    return common_path[0:-1] if common_path.endswith('.') else None


def get_parsed_json(template, json_doc):
    value = ''.join('[*]{}'.format(x) if x == '.' else x for x in template)
    jsonpath_expr = parse(value)
    value = value + '[*]'
    jsonpath_expr_list = parse(value)

    json_data = jsonpath_expr.find(json_doc)
    try:
        json_data_list = jsonpath_expr_list.find(json_doc)
    except Exception as e:
        print(e)
        json_data_list = []

    if len(json_data) > 0 and len(json_data_list) > 1:
        return [[match.value for match in jsonpath_expr_list.find(json_doc)]]
    else:
        try:
            return [jsonpath_expr.find(json_doc)[0].value]
        except IndexError:
            try:
                return [jsonpath_expr.find(json_doc['data'][0])[0].value]
            except Exception as e:
                return []


def transform_simple_object(json_doc, template):
    new_doc = {}
    if len(json_doc.keys()) == 0:
        return new_doc

    for key, value in template.items():
        if isinstance(value, str):
            try:
                val = get_parsed_json(value, json_doc)
            except IndexError:
                val = []
        else:
            val = []
            for element in value:
                try:
                    #jsonpath_expr.find(json_doc)[0].value
                    val.append(get_parsed_json(element, json_doc))
                except IndexError:
                    pass

        if isinstance(val, list):
            val = [item for item in val if item]

        if len(val) == 0:
            continue
        if len(val) == 1:
            val = val[0]
        new_doc[key] = val
    return new_doc


def transform_array_of_simple_object(json_doc, template):
    if isinstance(json_doc, list):
        return [transform_simple_object(_doc, template) for _doc in json_doc]
    return json_doc


def transform_complex_object(json_doc, template):
    new_doc = {}
    paths = extract_paths_from_template(template)
    common_path = find_longest_common_path(paths)
    if len(paths) == 1 and paths[0] == common_path:
        return transform_simple_object(json_doc, template)
    if common_path:
        try:
            trimmed_json_doc = get_parsed_json(common_path, json_doc)[0]
        except IndexError:
            trimmed_json_doc = None
            print("Index error")
        #trimmed_json_doc = [match.value for match in jsonpath_expr.find(json_doc)] #jsonpath_expr.find(json_doc)[0].value
        trimmed_template = remove_common_path_from_template(template, common_path)
    else:
        trimmed_json_doc = json_doc
        trimmed_template = template
    if not trimmed_json_doc:
        return {}
    if isinstance(trimmed_json_doc, list):
        new_doc = transform_array_of_simple_object(trimmed_json_doc, trimmed_template)
    else:
        new_doc = transform_simple_object(trimmed_json_doc, trimmed_template)
    return new_doc


def remove_common_path_from_template(template, common_path):
    if not isinstance(common_path, str):
        return template
    common_path = common_path + '.'
    new_template = {}
    for key,value in template.items():
        if isinstance(value, str):
            new_template[key] = value[len(common_path):] if value.startswith(common_path) else value
        else:
            new_value = []
            for path in value:
                trimmed_path = path[len(common_path):] if path.startswith(common_path) else path
                new_value.append(trimmed_path)
            new_template[key] = new_value
    return new_template


def is_array_of_string(_input):
    return isinstance(_input, list) and all([isinstance(i, str) for i in _input])


def separate_simple_an_complex_paths(template):
    simple_path_template = {}
    complex_path_template = {}
    for key, value in template.items():
        if isinstance(value, str) or is_array_of_string(value):
            simple_path_template[key] = value
        else:
            complex_path_template[key] = value
    return {
        'simple_path_template': simple_path_template,
        'complex_path_template': complex_path_template
    }
