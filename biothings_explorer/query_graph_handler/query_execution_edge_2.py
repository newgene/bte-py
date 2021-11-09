import functools
from .utils import remove_biolink_prefix, to_array
from .helper import QueryGraphHelper
from .biolink import BioLinkModelInstance


class UpdatedExeEdge:
    def __init__(self, q_edge, reverse=False, prev_edge=None):
        self.q_edge = q_edge
        self.connecting_nodes = []
        self.reverse = reverse
        self.prev_edge = prev_edge
        self.input_equivalent_identifiers = {}
        self.output_equivalent_identifiers = {}
        self.object = q_edge['object']
        self.subject = q_edge['subject']
        self.object_entity_count = None
        self.subject_entity_count = None
        self.executed = False
        self.logs = []
        self.results = []
        self.requires_intersection = False
        self.init()

    def init(self):
        self.check_initial_entity_count()
        self.check_connecting_nodes()
        self.check_if_results_need_intersection()

    def check_connecting_nodes(self):
        self.connecting_nodes.append(self.subject['id'])
        self.connecting_nodes.append(self.object['id'])

    def check_initial_entity_count(self):
        self.object_entity_count = self.object.has_input() if len(self.object['curie']) else None
        self.subject_entity_count = self.subject.has_input() if len(self.subject['curie']) else None

    def update_entity_count_by_id(self, node_id, entities):
        if self.subject['id'] == node_id:
            self.q_edge['subject']['curie'] = entities
            self.subject_entity_count = len(entities)
        elif self.object['id'] == node_id:
            self.q_edge['object']['curie'] = entities
            self.object_entity_count = len(entities)
        self.check_if_results_need_intersection()

    def check_if_results_need_intersection(self):
        self.requires_entity_count_choice = True if self.object_entity_count and self.subject_entity_count else False

    def choose_lower_entity_value(self):
        if self.object_entity_count and self.subject_entity_count:
            if self.object_entity_count > self.subject_entity_count:
                self.reverse = False
                self.q_edge['object'].pop('curie')
            else:
                self.reverse = True
                self.q_edge['subject'].pop('curie')

    def intersect_and_save_results(self, current_results, all_edges):
        for index, edge in enumerate(all_edges):
            if edge.get_id() == self.q_edge.get_id():
                if all_edges[index - 1]:
                    neighbor = all_edges[index - 1]
                    prev_edge_res = self.intersect_results(neighbor['results'], current_results)
                if all_edges[index + 1]:
                    neighbor = all_edges[index + 1]
                    next_edge_res = self.intersect_results(current_results, neighbor['results'])
        self.results = current_results

    def intersect_results(self, first, second):
        results = []
        dropped = 0
        for f in first:
            first_semantic_types = f['$input']['obj']
            for f_type in first_semantic_types:
                for s in second:
                    second_semantic_types = s['$input']['obj']
                    second_semantic_types = second_semantic_types + s['$output']['obj']
                    for s_type in second_semantic_types:
                        if f_type['_leafSemanticType'] == s_type['_leafSemanticType']:
                            f_ids = set()
                            for prefix in f_type['_dbIDs']:
                                f_ids.add(prefix + ':' + f_type['_dbIDs'][prefix])
                            s_ids = set()
                            for prefix in s_type['_dbIDs']:
                                s_ids.add(prefix + ':' + s_type['_dbIDs'][prefix])
                            for f_id in f_ids:
                                for s_id in s_ids:
                                    if f_id == s_id:
                                        results.append(f)
        dropped = len(first) + len(second) - len(results)
        return results

    def store_results(self, res):
        self.results = res

    def get_id(self):
        return self.q_edge.get_id()

    def get_hashed_edge_representation(self):
        to_be_hashed = self.get_subject().get_categories() + self.get_predicate() + self.get_object().get_categories() + self.get_input_curie()
        helper = QueryGraphHelper()
        return helper._generate_hash(to_be_hashed)

    def expand_predicates(self, predicates):
        reduced = functools.reduce(
            lambda prev, current: [*prev, *BioLinkModelInstance.get_descendant_predicates(current)], predicates, [])
        return list(set(reduced))

    def get_predicate(self):
        if not self.predicate:
            return None
        predicates = [remove_biolink_prefix(item) for item in to_array(self.predicate)]
        expanded_predicates = self.expand_predicates(predicates)
        mapped = [BioLinkModelInstance.reverse(predicate) if self.is_reversed() else predicate for predicate in expanded_predicates]
        return [item for item in mapped if item]

    def get_subject(self):
        if self.reverse:
            return self.q_edge['object']
        return self.q_edge['subject']

    def get_object(self):
        if self.reverse:
            return self.q_edge['subject']
        return self.q_edge['object']

    def is_reversed(self):
        return self.reverse

    def get_input_curie(self):
        curie = self.q_edge['subject'].get_curie() or self.q_edge['object'].get_curie()
        if isinstance(curie, list):
            return curie
        return [curie]

    def get_input_node(self):
        return self.q_edge['object'] if self.reverse else self.q_edge['subject']

    def get_output_node(self):
        return self.q_edge['subject'] if self.reverse else self.q_edge['object']

    def has_input_resolved(self):
        return len(self.input_equivalent_identifiers) != 0

    def has_input(self):
        if self.reverse:
            return self.q_edge['object'].has_input()
        return self.q_edge['subject'].has_input()
