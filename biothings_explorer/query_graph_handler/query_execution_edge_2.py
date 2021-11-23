import functools
import math
from .utils import remove_biolink_prefix, to_array
from .helper import QueryGraphHelper
from .biolink import BioLinkModelInstance
from .log_entry import LogEntry


class UpdatedExeEdge:
    def __init__(self, q_edge, reverse=False, prev_edge=None):
        self.q_edge = q_edge
        self.reverse = reverse
        self.prev_edge = prev_edge
        self.input_equivalent_identifiers = {}
        self.output_equivalent_identifiers = {}
        self.object = q_edge['object']
        self.subject = q_edge['subject']
        # self.object_entity_count = self.object['entity_count']
        # self.subject_entity_count = self.subject['entity_count']
        self.executed = False
        self.logs = []
        self.results = []

    def extract_curies_from_response(self, res, is_reversed):
        _all = {}
        types_to_include = self.q_edge['subject'].get_categories() if is_reversed else \
            self.q_edge['object'].get_categories()
        for result in res:
            for o in result['$input']['obj']:
                _type = o['_leafSemanticType']
                if _type in types_to_include or 'NamedThing' in types_to_include or _type in str(types_to_include):
                    if not _all.get(_type):
                        _all[_type] = {}
                    original = result['$input']['original']
                    if o.get('_dbIDs'):
                        original_aliases = set()
                        for prefix in o['_dbIDs']:
                            # original_aliases.add(prefix + ':' + o['_dbIDs'][prefix])
                            if isinstance(o['_dbIDs'].get(prefix), list):
                                for single_alias in o['_dbIDs'][prefix]:
                                    if ':' in single_alias:
                                        original_aliases.add(single_alias)
                                    else:
                                        original_aliases.add(prefix + ':' + single_alias)
                            else:
                                if ':' in o['_dbIDs'][prefix]:
                                    original_aliases.add(o['_dbIDs'][prefix])
                                else:
                                    original_aliases.add(prefix + ':' + o['_dbIDs'][prefix])
                        original_aliases = [*original_aliases]
                        was_found = False
                        for alias in original_aliases:
                            if _all[_type].get(alias):
                                was_found = True
                        if not was_found:
                            _all[_type][original] = original_aliases
                    elif o.get('curie'):
                        if isinstance(o['curie'], list):
                            _all[_type][original] = o['curie']
                        else:
                            _all[_type][original] = [o['curie']]
                    else:
                        _all[_type][original] = [original]
            for o in result['$output']['obj']:
                _type = o['_leafSemanticType']
                if _type in types_to_include or 'NamedThing' in types_to_include or _type in str(types_to_include):
                    if not _all.get(_type):
                        _all[_type] = {}
                    original = result['$output']['original']
                    if o.get('_dbIDs'):
                        original_aliases = set()
                        for prefix in o['_dbIDs']:
                            # original_aliases.add(prefix + ':' + o['_dbIDs'][prefix])
                            if isinstance(o['_dbIDs'].get(prefix), list):
                                for single_alias in o['_dbIDs'][prefix]:
                                    if ':' in single_alias:
                                        original_aliases.add(single_alias)
                                    else:
                                        original_aliases.add(prefix + ':' + single_alias)
                            else:
                                if ':' in o['_dbIDs'][prefix]:
                                    original_aliases.add(o['_dbIDs'][prefix])
                                else:
                                    original_aliases.add(prefix + ':' + o['_dbIDs'][prefix])
                        original_aliases = [*original_aliases]
                        was_found = False
                        for alias in original_aliases:
                            if _all[_type].get(alias):
                                was_found = True
                        if not was_found:
                            _all[_type][original] = original_aliases
                    elif o.get('curie'):
                        if isinstance(o['curie'], list):
                            _all[_type][original] = o['curie']
                        else:
                            _all[_type][original] = [o['curie']]
                    else:
                        _all[_type][original] = [original]
        return _all

    def _combine_curies(self, curies):
        combined = {}
        for _type in curies:
            for original in curies[_type]:
                combined[original] = curies[_type][original]
        return combined

    def update_nodes_curies(self, res):
        curies_by_semantic_type = self.extract_curies_from_response(res, self.reverse)
        combined_curies = self._combine_curies(curies_by_semantic_type)
        if self.reverse:
            self.q_edge.subject.update_curies(combined_curies)
        else:
            self.q_edge.object.update_curies(combined_curies)

        curies_by_semantic_type_2 = self.extract_curies_from_response(res, not self.reverse)
        combined_curies_2 = self._combine_curies(curies_by_semantic_type_2)
        if self.reverse:
            self.q_edge.subject.update_curies(combined_curies_2)
        else:
            self.q_edge.object.update_curies(combined_curies_2)

    def apply_node_constraints(self):
        kept = []
        save_kept = False
        sub_constraints = self.subject['constraints']
        if sub_constraints and len(sub_constraints):
            _from = '$output' if self.reverse else '$input'
            save_kept = True
            for i in range(len(self.results)):
                res = self.results[i]
                keep = True
                for x in range(len(sub_constraints)):
                    constraint = sub_constraints[x]
                    keep = self.meets_constraint(constraint, res, _from)
                if keep:
                    kept.append(res)
        obj_constraints = self.object['constraints']
        if obj_constraints and len(obj_constraints):
            _from = '$input' if self.reverse else '$output'
            save_kept = True
            for i in range(len(self.results)):
                res = self.results[i]
                keep = True
                for x in range(len(obj_constraints)):
                    constraint = obj_constraints[x]
                    keep = self.meets_constraint(constraint, res, _from)
                if keep:
                    kept.append(res)
        if save_kept:
            self.results = kept
        else:
            pass

    def meets_constraint(self, constraint, result, _from):
        available_attributes = set()
        for key in result[_from]['obj'][0]['attributes']:
            available_attributes.add(key)
        available_attributes = [*available_attributes]
        filters_found = [attr for attr in available_attributes if attr == constraint['id']]
        if not len(filters_found):
            return False
        else:
            node_attributes = []
            for _filter in filters_found:
                node_attributes[_filter] = result[_from]['obj'][0]['attributes'][_filter]
            if constraint['operator'] == '==':
                for key in node_attributes:
                    if not math.isnan(constraint['value']):
                        if isinstance(node_attributes[key], list):
                            if constraint['value'] in node_attributes[key] or \
                                    str(constraint['value']) in node_attributes[key]:
                                return True
                        else:
                            if node_attributes[key] == constraint['value'] or \
                                    node_attributes[key] == str(constraint['value']) or \
                                    node_attributes[key] == int(constraint['value']):
                                return True
                    else:
                        if isinstance(node_attributes[key], list):
                            if constraint['value'] in node_attributes[key]:
                                return True
                        else:
                            if node_attributes[key] == constraint['value'] or \
                                    node_attributes[key] == str(constraint['value']) or \
                                    node_attributes[key] == int(constraint['value']):
                                return True
                return False
            elif constraint['operator'] == '>':
                for key in node_attributes:
                    if isinstance(node_attributes[key], list):
                        for index in range(len(node_attributes[key])):
                            element = node_attributes[key][index]
                            if int(element) > int(constraint['value']):
                                return True
                    else:
                        if int(node_attributes[key]) > int(constraint['value']):
                            return True
                return False
            elif constraint['operator'] == '>=':
                for key in node_attributes:
                    if isinstance(node_attributes[key], list):
                        for index in range(len(node_attributes[key])):
                            element = node_attributes[key][index]
                            if int(element) >= int(constraint['value']):
                                return True
                    else:
                        if int(node_attributes[key]) >= int(constraint['value']):
                            return True
                return False
            elif constraint['operator'] == '<':
                for key in node_attributes:
                    if isinstance(node_attributes[key], list):
                        for index in range(len(node_attributes[key])):
                            element = node_attributes[key][index]
                            if int(element) > int(constraint['value']):
                                return True
                    else:
                        if int(node_attributes[key]) < int(constraint['value']):
                            return True
                return False
            elif constraint['operator'] == '<=':
                for key in node_attributes:
                    if isinstance(node_attributes[key], list):
                        for index in range(len(node_attributes[key])):
                            element = node_attributes[key][index]
                            if int(element) <= int(constraint['value']):
                                return True
                    else:
                        if int(node_attributes[key]) <= int(constraint['value']):
                            return True
                return False
            else:
                return False

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
        self.requires_entity_count_choice = True if self.object['entity_count'] and self.subject[
            'entity_count'] else False

    def choose_lower_entity_value(self):
        if self.q_edge['object']['entity_count'] and self.q_edge['subject']['entity_count']:
            if self.q_edge['object']['entity_count'] == self.q_edge['subject']['entity_count']:
                self.reverse = False
                self.q_edge['object'].hold_curie()
            elif self.q_edge['object']['entity_count'] > self.q_edge['subject']['entity_count']:
                self.reverse = False
                self.q_edge['object'].hold_curie()
            else:
                self.reverse = True
                self.q_edge['subject'].hold_curie()
        else:
            pass

    def store_results(self, res):
        self.results = res
        self.apply_node_constraints()
        self.update_nodes_curies(res)

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
        if not self.q_edge.predicate:
            return None
        predicates = [remove_biolink_prefix(item) for item in to_array(self.q_edge.predicate)]
        expanded_predicates = self.expand_predicates(predicates)
        mapped = [BioLinkModelInstance.reverse(predicate) if self.is_reversed() else predicate for predicate in
                  expanded_predicates]
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
