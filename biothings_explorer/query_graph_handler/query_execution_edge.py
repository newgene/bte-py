import functools
from .helper import QueryGraphHelper
from .utils import to_array, get_unique, remove_biolink_prefix
from .biolink import BioLinkModelInstance


class QExeEdge:
    def __init__(self, qEdge, reverse=False, prev_edge=None):
        self.q_edge = qEdge
        self.reverse = reverse
        self.prev_edge = prev_edge
        self.input_equivalent_identifiers = {}
        self.output_equivalent_identifiers = {}

    def get_id(self):
        return self.q_edge.get_id()

    def get_hashed_edge_representation(self):
        to_be_hashed = self.get_subject().get_categories() + self.get_predicate() + self.get_object().get_categories() + self.get_input_curie()
        helper = QueryGraphHelper()
        return helper._generate_hash(to_be_hashed)

    def expand_predicates(self, predicates):
        reduced = functools.reduce(
            lambda prev, current: [*prev, *BioLinkModelInstance.get_descendant_predicates(current)], predicates, [])
        return [item for item in set(reduced)]

    def get_predicate(self):
        if not hasattr(self, 'predicate'):
            return None
        predicates = [remove_biolink_prefix(item) for item in to_array(self.predicate)]
        expanded_predicates = self.expand_predicates(predicates)
        return [BioLinkModelInstance.reverse(predicate) if self.is_reversed() else predicate for predicate in expanded_predicates if predicate]

    def get_subject(self):
        if self.reverse:
            return self.q_edge.object
        return self.q_edge.subject

    def get_object(self):
        if self.reverse:
            return self.q_edge.subject
        return self.q_edge.object

    def is_reversed(self):
        return self.reverse

    def get_input_curie(self):
        curie = self.q_edge.subject.get_curie() or self.q_edge.object.get_curie()
        if isinstance(curie, list):
            return curie
        return [curie]

    def get_input_node(self):
        return self.q_edge.object if self.reverse else self.q_edge.subject

    def get_output_node(self):
        return self.q_edge.subject if self.reverse else self.q_edge.object

    def has_input_resolved(self):
        return not (len(self.input_equivalent_identifiers) == 0)

    def has_input(self):
        if self.reverse:
            return self.q_edge.object.has_input()
        return self.q_edge.subject.has_input()
