import functools
from .helper import QueryGraphHelper
from .utils import to_array, get_unique, remove_biolink_prefix
from .biolink import BioLinkModelInstance


class QEdge:
    def __init__(self, _id, info):
        self.id = _id
        self.predicate = info.get('predicates')
        self.subject = info.get('subject')
        self.object = info.get('object')
        self.expanded_predicates = []
        self.init()

    def init(self):
        self.expanded_predicates = self.get_predicate()

    def get_id(self):
        return self.id

    def get_hashed_edge_representation(self):
        to_be_hashed = self.subject.get_categories() + self.predicate + self.object.get_categories() + self.get_input_curie()
        helper = QueryGraphHelper()
        return helper._generate_hash(to_be_hashed)

    def expand_predicates(self, predicates):
        reduced = functools.reduce(lambda prev, current: [*prev, *BioLinkModelInstance.get_descendant_predicates(current)], predicates, [])
        return [item for item in set(reduced)]

    def get_predicate(self):
        if not self.predicate:
            return None
        predicates = [remove_biolink_prefix(item) for item in to_array(self.predicate)]
        expanded_predicates = self.expand_predicates(predicates)
        return [BioLinkModelInstance.reverse(predicate) if self.is_reversed() else predicate for predicate in expanded_predicates if predicate]

    def get_subject(self):
        if self.is_reversed():
            return self.object
        return self.subject

    def get_object(self):
        if self.is_reversed():
            return self.subject
        return self.object

    def is_reversed(self):
        return not self.subject.get_curie() and self.object.get_curie()

    def get_input_curie(self):
        curie = self.subject.get_curie() or self.object.get_curie()
        if isinstance(curie, list):
            return curie
        return [curie]

    def get_input_node(self):
        return self.object if self.is_reversed() else self.subject

    def get_output_node(self):
        return self.subject if self.is_reversed() else self.object

    def has_input_resolved(self):
        if self.is_reversed():
            return self.object.has_equivalent_ids()
        return self.subject.has_equivalent_ids()

    def has_input(self):
        if self.is_reversed():
            return self.object.has_input()
        return self.subject.has_input()
