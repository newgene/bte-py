from abc import ABC
from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity


class BaserResolver(ABC):
    def annotate_unresolved_inputs(self, unresolved_inputs, current_result):
        for semantic_type in unresolved_inputs:
            for curie in unresolved_inputs[semantic_type]:
                if curie not in current_result:
                    current_result[curie] = []
                current_result[curie].append(IrresolvableBioEntity(semantic_type, curie))
        return current_result

    def resolve(self, usr_input):
        pass
