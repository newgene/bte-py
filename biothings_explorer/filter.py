import copy
from .config import FILTER_FIELDS


def get_unique_vals_for_each_field(operations = []):
    all_values = {}
    for field in FILTER_FIELDS:
        all_values[field] = set()
    for operation in operations:
        for field in FILTER_FIELDS:
            all_values[field].add(operation.association[field])
    return all_values


def ft(ops, criteria):
    all_values = get_unique_vals_for_each_field(ops)
    filters = {}

    for field in FILTER_FIELDS:
        if not (field in criteria) or not criteria[field]:
            filters[field] = all_values[field]

    res = copy.deepcopy(ops)
    res = [rec for rec in res if filters[field] in rec.association[field]]
    return res
