import functools
from .utils import to_array, remove_biolink_prefix, get_unique
from .biolink import BioLinkModelInstance
from .exceptions.invalid_query_graph_error import InvalidQueryGraphError


class QNode:
    def __init__(self, _id, info):
        self.id = _id
        self.category = info['categories'] or 'NamedThing'
        self.curie = info.get('ids')
        self.entity_count = len(info.get('ids')) if info.get('ids') else 0
        self.held_curie = []
        self.held_expanded = {}
        self.constraints = info.get('constraints')
        self.connected_to = set()
        self.expand_curie()
        self.validate_constraints()

    def validate_constraints(self):
        required = ['id', 'operator', 'value']
        if self.constraints and len(self.constraints):
            for constraint in self.constraints:
                constraint_keys = constraint.keys()
                intersection = list(set(constraint_keys) & set(required))
                if len(intersection) < 3:
                    raise InvalidQueryGraphError(f"Invalid constraint specification must include ({required})")

    def expand_curie(self):
        if self.curie and len(self.curie):
            for _id in self.curie:
                if isinstance(_id, dict) and not _id.get(self.expanded_curie):
                    self.expanded_curie[_id] = [_id]

    def update_curies(self, curies):
        if not self.curie:
            self.curie = []
        if len(self.held_curie):
            self.curie = self.held_curie
            self.expanded_curie = self.held_expanded
            self.held_curie = []
            self.held_expanded = {}
        if not len(self.curie):
            self.curie = curies.keys()
            self.expanded_curie = curies
        else:
            self.intersect_with_expanded_curies(curies)
        self.entity_count = len(self.curie)

    def intersect_with_expanded_curies(self, new_curies):
        keep = {}
        for main_id in new_curies:
            current_list_of_aliases = new_curies[main_id]
            for existing_main_id in self.expanded_curie:
                existing_list_of_aliases = self.expanded_curie[existing_main_id]
                ids_match_found = list(set(current_list_of_aliases) & set(existing_list_of_aliases))
                if len(ids_match_found):
                    if not keep.get(main_id):
                        keep[main_id] = current_list_of_aliases
        self.expanded_curie = keep
        self.curie = keep.keys()

    def hold_curie(self):
        self.held_curie = self.curie
        self.held_expanded = self.expanded_curie
        self.curie = None
        self.expanded_curie = {}

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

    def update_connection(self, edge_id):
        self.connected_to.add(edge_id)

    def get_connections(self):
        return list(self.connected_to)

    def has_input(self):
        return True if self.curie else False

    def has_equivalent_ids(self):
        return True if hasattr(self, 'equivalent_ids') else False

    def get_entity_count(self):
        return len(self.curie) if self.curie else 0
