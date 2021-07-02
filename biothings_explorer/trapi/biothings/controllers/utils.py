import re


def to_array(_input):
    if isinstance(_input, list):
        return _input
    return [_input]


def get_unique(_input):
    return list(dict.fromkeys(_input))


def remove_bio_link_prefix(_input):
    if _input and _input.startswith('biolink:'):
        return _input[8:]
    return _input


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
