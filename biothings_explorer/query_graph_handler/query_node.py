import functools
from .utils import to_array, remove_biolink_prefix, get_unique
from .biolink import BioLinkModelInstance


class QNode:
    def __init__(self, _id, info):
        self.id = _id
        self.category = info.get('categories') or info.get('category') or 'NamedThing'
        self.curie = info.get('ids') or info.get('id')

    def get_id(self):
        return self.id

    def get_curie(self):
        return self.curie

    def get_equivalent_ids(self):
        return self.equivalent_ids

    def get_categories(self):
        if not self.has_equivalent_ids():
            categories = to_array(self.category)
            expanded_categories = []
            for category in categories:
                expanded_categories = [
                    *expanded_categories,
                    *BioLinkModelInstance.get_descendant_classes(remove_biolink_prefix(category))
                ]
            return get_unique(expanded_categories)
        categories = []
        for entities in self.equivalent_ids.values():
            for entity in entities:
                categories = [*categories, *entity['semanticTypes']]
        return get_unique(categories)

    def get_entities(self):
        reduced = functools.reduce(
            lambda prev, current: [*prev, *current], self.equivalent_ids.values(), [])
        return reduced

    def get_primary_ids(self):
        return [entity['primaryID'] for entity in self.get_entities()]

    def set_equivalent_ids(self, equivalent_ids):
        self.equivalent_ids = equivalent_ids

    def update_equivalent_ids(self, equivalent_ids):
        if not hasattr(self, 'equivalent_ids'):
            self.equivalent_ids = equivalent_ids
        else:
            self.equivalent_ids = {**self.equivalent_ids, **equivalent_ids}

    def has_input(self):
        return self.curie

    def has_equivalent_ids(self):
        if hasattr(self, 'equivalent_ids'):
            return self.equivalent_ids
        return None
