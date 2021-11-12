import functools
from .utils import remove_biolink_prefix, to_array
from .helper import QueryGraphHelper
from .biolink import BioLinkModelInstance
from .log_entry import LogEntry


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
        #self.object_entity_count = self.object['entity_count']
        #self.subject_entity_count = self.subject['entity_count']
        self.executed = False
        self.logs = []
        self.results = []
        self.requires_intersection = False

    def extract_curies_from_response(self, res):
        _all = {}
        for result in res:
            for o in result['$input']['obj']:
                _type = o['_leafSemanticType']
                if not _all.get(_type):
                    _all[_type] = {}
                original = result['$input']['original']
                original_aliases = set()
                for prefix in o['_dbIDs']:
                    original_aliases.add(prefix + ':' + o['_dbIDs'][prefix])
                original_aliases = [*original_aliases]
                was_found = False
                for alias in original_aliases:
                    if _all[_type].get(alias):
                        was_found = True
                if not was_found:
                    _all[_type][original] = original_aliases
            for o in result['$output']['obj']:
                _type = o['_leafSemanticType']
                if not _all.get(_type):
                    _all[_type] = {}
                original = result['$output']['original']
                original_aliases = set()
                for prefix in o['_dbIDs']:
                    original_aliases.add(prefix + ':' + o['_dbIDs'][prefix])
                original_aliases = [*original_aliases]
                was_found = False
                for alias in original_aliases:
                    if _all[_type].get(alias):
                        was_found = True
                if not was_found:
                    _all[_type][original] = original_aliases
        return _all

    def update_node_curies(self, res):
        curies_by_semantic_type = self.extract_curies_from_response(res)
        self.process_curies(curies_by_semantic_type)

    def process_curies(self, curies):
        for semantic_type in curies:
            self.find_node_and_add_curie(curies[semantic_type], semantic_type)

    def find_node_and_add_curie(self, curies, semantic_type):
        sub_cat = str(self.q_edge['subject']['category'])
        obj_cat = str(self.q_edge['object']['category'])
        if semantic_type in sub_cat:
            self.q_edge['subject'].update_curies(curies)
        elif semantic_type in obj_cat:
            self.q_edge['object'].update_curies(curies)
        else:
            if 'NamedThing' in sub_cat:
                self.q_edge['subject'].update_curies(curies)
            elif 'NamedThing' in obj_cat:
                self.q_edge['object'].update_curies(curies)
            else:
                pass

    # def check_connecting_nodes(self):
    #     self.connecting_nodes.append(self.subject['id'])
    #     self.connecting_nodes.append(self.object['id'])

    # def check_initial_entity_count(self):
    #     self.object_entity_count = self.object.has_input() if len(self.object['curie']) else None
    #     self.subject_entity_count = self.subject.has_input() if len(self.subject['curie']) else None

    # def update_entity_count_by_id(self, node_id, entities):
    #     if self.subject['id'] == node_id:
    #         self.q_edge['subject']['curie'] = entities
    #         self.subject_entity_count = len(entities)
    #     elif self.object['id'] == node_id:
    #         self.q_edge['object']['curie'] = entities
    #         self.object_entity_count = len(entities)
    #     self.check_if_results_need_intersection()

    def check_if_results_need_intersection(self):
        self.requires_entity_count_choice = True if self.object['entity_count'] and self.subject['entity_count'] else False

    def choose_lower_entity_value(self):
        if self.object['entity_count'] and self.subject['entity_count']:
            if self.object['entity_count'] == self.subject['entity_count']:
                self.reverse = False
                self.held_subject_curies = self.q_edge['subject']['curie']
                #TODO delete this?
                self.q_edge['subject'].hold_curie()

            elif self.object['entity_count'] > self.subject['entity_count']:
                self.reverse = False
                self.q_edge['object'].hold_curie()
            else:
                self.reverse = True
                self.q_edge['subject'].hold_curie()
        else:
            pass

    def store_results(self, res):
        self.results = res
        self.update_node_curies(res)

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
