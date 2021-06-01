from abc import ABC
from biothings_explorer.biomedical_id_resolver.common.exceptions import IrresolvableIDResolverInputError


class BaseValidator(ABC):
    user_input = {}
    _irresolvable = {}
    _resolvable = {}

    def __init__(self, user_input):
        self.user_input = user_input
        self._irresolvable = {}
        self._resolvable = {}

    @property
    def irresolvable(self):
        return self._irresolvable

    @property
    def resolvable(self):
        return self._resolvable

    def validate_if_input_is_object(self, user_input):
        user_input = user_input if user_input else self.user_input
        if not isinstance(user_input, dict):
            raise IrresolvableIDResolverInputError('Your Input to ID Resolver is Irresolvable. It should be a plain object!')

    def validate_if_values_of_input_is_array(self, user_input):
        user_input = user_input if user_input else self.user_input
        for vals in user_input.values():
            if not isinstance(vals, list):
                raise IrresolvableIDResolverInputError("Your Input to ID Resolver is Irresolvable. All values of your input dictionary should be a list!")

    def valideate_if_each_item_in_input_values_is_curie(self, user_input):
        user_input = user_input if user_input else self.user_input
        for vals in user_input.values():
            for item in vals:
                if not isinstance(item, str) or ':' not in item:
                    raise IrresolvableIDResolverInputError(
                        f"Your Input to ID Resolver is Irresolvable. Each item in the values of your input dictionary should be a curie. Spotted {item} is not a curie")

    def check_if_comma_in_input(self, user_input):
        user_input = user_input if user_input else self.user_input
        for key in user_input:
            irresolvable = []
            for item in user_input[key]:
                if isinstance(item, str) and ',' in item:
                    irresolvable.append(item)
            user_input[key] = [item for item in user_input[key] if item not in irresolvable]
            if len(irresolvable) > 0:
                self._irresolvable[key] = irresolvable
        return user_input

    def validate_input_structure(self):
        self.validate_if_input_is_object(self.user_input)
        self.validate_if_values_of_input_is_array(self.user_input)
        self.valideate_if_each_item_in_input_values_is_curie(self.user_input)
        self.user_input = self.check_if_comma_in_input(self.user_input)

    def validate(self):
        pass
