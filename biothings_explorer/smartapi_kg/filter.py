import copy
from collections.abc import Iterable
from .config import FILTER_FIELDS


def get_unique_vals_for_each_field(operations = []):
    all_values = {}
    for field in FILTER_FIELDS:
        all_values[field] = set()
    for operation in operations:
        for field in FILTER_FIELDS:
            all_values[field].add(operation.get('association', {}).get(field))
    return all_values


def ft(ops, criteria):
    all_values = get_unique_vals_for_each_field(ops)
    filters = {}

    for field in FILTER_FIELDS:
        if not (field in criteria) or not criteria[field]:
            filters[field] = all_values[field]
        else:
            vals = criteria[field] if isinstance(criteria[field], list) else [criteria[field]]
            filters[field] = set(vals)

    res = copy.deepcopy(ops)
    for field in FILTER_FIELDS:
        res = [rec for rec in res if rec['association'].get(field) in filters.get(field)]

    return res
