from biothings_explorer.biomedical_id_resolver.validate.biolink_based_validator import BioLinkBasedValidator
from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity


def annotate_unresolved_inputs(unresolved_inputs, current_result):
    for semantic_type in unresolved_inputs.keys():
        for curie in unresolved_inputs[semantic_type]:
            if curie not in current_result:
                current_result[curie] = []
            current_result[curie].append(IrresolvableBioEntity(semantic_type, curie))
    return current_result


def generate_invalid(user_input):
    validator = BioLinkBasedValidator(user_input)
    validator.validate()
    result = annotate_unresolved_inputs(validator.valid, {})
    return result
