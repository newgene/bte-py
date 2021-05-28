from .config import CURIE, APIMETA


def generate_curie(prefix, val):
    if prefix in CURIE['ALWAYS_PREFIXED']:
        return str(val)
    else:
        return prefix + ':' + str(val)


def get_prefix_from_curie(curie):
    return curie.split(':')[0]


def generate_db_id(val):
    if val.split(':')[0] not in CURIE['ALWAYS_PREFIXED']:
        try:
            index = val.index(':') + 1
        except ValueError as e:
            index = 0
        return val[index:]
    else:
        return val


def is_numeric(val):
    try:
        return isinstance(val, int) or isinstance(val, float) or val.isnumeric()
    except Exception as e:
        print(e)
    return False


def append_array_or_non_array_object_to_array(lst, item):
    if isinstance(item, list):
        for val in item:
            if isinstance(val, str):
                lst.append(val)
            elif is_numeric(val):
                lst.append(str(val))
        return lst
    else:
        if isinstance(item, str):
            lst.append(item)
        elif is_numeric(item):
            lst.append(str(item))
        return lst


def generate_object_with_no_duplicate_elements_in_value(_input):
    for key in _input:
        _input[key] = [item for item in set(_input[key])]
    return _input


def generate_id_type_dict():
    res = {}
    for metadata in APIMETA.values():
        for prefix in metadata['id_ranks']:
            if prefix not in res:
                res[prefix] = []
            res[prefix].append(metadata['semantic'])
    return res
