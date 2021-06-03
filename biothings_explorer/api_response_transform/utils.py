def generate_curie(id_type, _id):
    if isinstance(_id, list):
        _id = _id[0]
    if isinstance(_id, str) and ':' in _id:
        _id = _id.split(':')[-1]
    return id_type + ':' + _id


def to_array(item):
    if not isinstance(item, list):
        return [item]
    return item
