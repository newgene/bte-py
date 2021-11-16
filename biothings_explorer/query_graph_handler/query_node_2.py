import functools
from .utils import to_array, remove_biolink_prefix, get_unique
from .biolink import BioLinkModelInstance


class QNode:
    def __init__(self, _id, info):
        self.id = _id
        self.category = info['categories'] or 'NamedThing'
        self.curie = info['ids']
        self.entity = info['ids']
        self.entity_count = len(info['ids']) if info['ids'] else 0
        self.held_curie = []
        self.connected_to = set()

    # def update_curies(self, curies):
    #     if not self.curie:
    #         self.curie = []
    #     if len(self.curie):
    #         self.curie = list(set(self.curie) & set(curies))
    #     else:
    #         self.curie = curies
    #     self.entity_count = len(self.curie)

    def update_curies(self, curies):
        if not self.curie:
            self.curie = []
        if len(self.held_curie):
            self.curie = self.held_curie
            self.held_curie = []
        # if self._is_broad_type():
        #     self.curie = [*self.curie, *curies.keys()]
        if not len(self.curie):
            self.curie = curies.keys()
        else:
            if not len(self.curie):
                self.curie = curies.keys()
            else:
                intersection = self.intersect_curies(self.curie, curies)
                self.curie = intersection
        self.entity_count = len(self.curie)

    def hold_curie(self):
        self.held_curie = self.curie
        self.curie = None

    def _combine_curies_into_list(self, curies):
        combined = set()
        for original in curies:
            if not isinstance(curies[original], list):
                combined.add(curies[original])
            else:
                for curie in curies[original]:
                    combined.add(curie)
        return list(combined)

    def intersect_curies(self, curies, new_curies):
        all_new_curies = self._combine_curies_into_list(new_curies)
        return list(set(curies) & set(all_new_curies))

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
                categories = [*categories, *entity['semantic_types']]
        return get_unique(categories)

    def get_entities(self):
        reduced = functools.reduce(
            lambda prev, current: [*prev, *current], self.equivalent_ids.values(), [])
        return reduced

    def get_primary_ids(self):
        return [entity['primary_id'] for entity in self.get_entities()]

    def set_equivalent_ids(self, equivalent_ids):
        self.equivalent_ids = equivalent_ids

    def update_equivalent_ids(self, equivalent_ids):
        if not self.equivalent_ids:
            self.equivalent_ids = equivalent_ids
        else:
            self.equivalent_ids = {**self.equivalent_ids, **equivalent_ids}

    def update_connection(self, edge_id):
        self.connected_to.add(edge_id)

    def get_connections(self):
        return list(self.connected_to)

    def has_input(self):
        return True if self.curie else False

    def has_equivalent_ids(self):
        return True if self.equivalent_ids else False
