def to_array(_input):
    if isinstance(_input, list):
        return _input
    return [_input]


def get_unique(_input):
    return [item for item in set(_input)]


def remove_biolink_prefix(_input):
    if _input and _input.startswith('biolink:'):
        return _input[8:]
    return _input
