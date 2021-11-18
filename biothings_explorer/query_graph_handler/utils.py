import itertools


def to_array(_input):
    if isinstance(_input, list):
        return _input
    return [_input]


def get_unique(_input):
    # set does not maintain order so we don't use it
    # [item for item in set(_input)]
    return list(dict.fromkeys(_input))


def remove_biolink_prefix(_input):
    if _input and _input.startswith('biolink:'):
        return _input[8:]
    return _input


def intersection(set_a, set_b):
    result_set = set()
    for elem in set_b:
        if elem in set_a:
            result_set.add(elem)
    return result_set


def cartesian(a):
    # i = []
    # j = []
    # l = []
    # m = []
    # a1 = []
    # o = []
    #
    # if not a or len(a == 0):
    #     return a
    #
    # a1 = a[0:1][0]
    # a = cartesian(a)
    #
    result = list(itertools.product(*a))
    return result
