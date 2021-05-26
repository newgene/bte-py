from .base_validator import BaseValidator
from ..biolink import BioLinkHandlerInstance
from ..utils import get_prefix_from_curie
from ..config import APIMETA


class BioLinkBasedValidator(BaseValidator):
    _biolink = {}
    _valid = {}

    def __init__(self, user_input):
        super(BioLinkBasedValidator, self).__init__(user_input)
        self._biolink = BioLinkHandlerInstance
        self._valid = {}
        self._resolvable = {}
        self._irresolvable = {}

    @property
    def valid(self):
        return self._valid

    def check_if_type_defined_in_bio_link(self, user_input):
        tmp = {}
        for semantic_type in user_input:
            if semantic_type in self._biolink.class_tree.objects:
                tmp[semantic_type] = user_input[semantic_type]
            else:
                self._irresolvable[semantic_type] = user_input[semantic_type]
        return tmp

    def group_dbids_by_prefix(self, user_input):
        tmp = {}
        for semantic_type in user_input:
            if semantic_type not in tmp:
                tmp[semantic_type] = {}
            for curie in user_input[semantic_type]:
                prefix = get_prefix_from_curie(curie)
                if prefix not in tmp[semantic_type]:
                    tmp[semantic_type][prefix] = []
                tmp[semantic_type][prefix].append(curie)
        return tmp

    def check_if_semantic_type_and_prefix_defined_in_config(self, semantic_type, prefix):
        if semantic_type in APIMETA and prefix in APIMETA[semantic_type]['mapping']:
            return True
        return False

    def add_valid_input_to_resolvable(self, semantic_type, prefix, curies):
        if semantic_type not in self._resolvable:
            self._resolvable[semantic_type] = []
        self._resolvable[semantic_type] = [*self._resolvable[semantic_type], *curies]

    def add_valid_input_to_irresolvable(self, semantic_type, prefix, curies):
        if semantic_type not in self._irresolvable:
            self._irresolvable[semantic_type] = []
        self._irresolvable[semantic_type] = [*self._irresolvable[semantic_type], *curies]

    def get_descendant_classes_with_given_id_prefix(self, semantic_type, prefix):
        descendants = self._biolink.class_tree.get_descendants(semantic_type)
        valid_descendants = [d for d in descendants if d.id_prefixes and prefix in d.id_prefixes]
        return [d.name for d in valid_descendants]

    def classify_a_semantic_type_and_prefix_pair(self, semantic_type, prefix, curies):
        can_be_resolved = False
        if self.check_if_semantic_type_and_prefix_defined_in_config(semantic_type, prefix):
            self.add_valid_input_to_resolvable(semantic_type, prefix, curies)
            can_be_resolved = True
        else:
            self.add_valid_input_to_irresolvable(semantic_type, prefix, curies)
        return can_be_resolved

    def classify(self, user_input):
        _input = self.group_dbids_by_prefix(user_input)
        for semantic_type in _input:
            for prefix in _input[semantic_type]:
                can_be_resolved = False
                if self.check_if_semantic_type_and_prefix_defined_in_config(semantic_type, prefix):
                    self.add_valid_input_to_resolvable(semantic_type, prefix, _input[semantic_type][prefix])
                    can_be_resolved = True
                valid_descendants = self.get_descendant_classes_with_given_id_prefix(semantic_type, prefix)
                for d in valid_descendants:
                    resolvable = self.classify_a_semantic_type_and_prefix_pair(d, prefix, _input[semantic_type][prefix])
                    if resolvable:
                        can_be_resolved = True
                if not can_be_resolved:
                    self.add_valid_input_to_irresolvable(semantic_type, prefix, _input[semantic_type][prefix])

    def validate(self):
        self.validate_input_structure()
        self._valid = self.check_if_type_defined_in_bio_link(self.user_input)
        self.classify(self._valid)
