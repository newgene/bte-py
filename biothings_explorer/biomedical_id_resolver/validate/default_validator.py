from .base_validator import BaseValidator
from biothings_explorer.biomedical_id_resolver.config import APIMETA
from biothings_explorer.biomedical_id_resolver.utils import get_prefix_from_curie, generate_id_type_dict


class DefaultValidator(BaseValidator):
    def handle_undefined_ids(self, user_input):
        if None not in user_input or 'undefined' not in user_input:
            return user_input

        id_type_dict = generate_id_type_dict()
        identified = []
        for curie in user_input['undefined']:
            prefix = get_prefix_from_curie(curie)
            possible_semantic_types = id_type_dict[prefix]
            if possible_semantic_types is None:
                continue
            for semantic_type in possible_semantic_types:
                if semantic_type not in user_input:
                    user_input[semantic_type] = []
                user_input[semantic_type].append(curie)
            identified.append(curie)
        user_input['undefined'] = [item for item in user_input['undefined'] if item not in identified]
        return user_input

    def check_if_semantic_type_can_be_resolved(self, user_input):
        dbids_with_correct_semantic_types = {}
        for semantic_type in user_input:
            if semantic_type in APIMETA.keys():
                dbids_with_correct_semantic_types[semantic_type] = user_input[semantic_type]
            else:
                self._irresolvable[semantic_type] = user_input[semantic_type]
        return dbids_with_correct_semantic_types

    def check_if_prefix_can_be_resolved(self, user_input):
        for semantic_type in user_input.keys():
            for item in user_input[semantic_type]:
                if get_prefix_from_curie(item) not in APIMETA[semantic_type]['mapping']:
                    if semantic_type not in self._irresolvable:
                        self._irresolvable[semantic_type] = []
                    self._irresolvable[semantic_type].append(item)
                else:
                    if semantic_type not in self._resolvable:
                        self._resolvable[semantic_type] = []
                    self._resolvable[semantic_type].append(item)

    def validate(self):
        self.validate_input_structure()
        restructured_input = self.handle_undefined_ids(self.user_input)
        tmp_resolvable_res = self.check_if_semantic_type_can_be_resolved(restructured_input)
        self.check_if_prefix_can_be_resolved(tmp_resolvable_res)
