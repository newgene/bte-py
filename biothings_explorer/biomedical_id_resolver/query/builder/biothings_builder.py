from biothings_explorer.biomedical_id_resolver.config import APIMETA, TIMEOUT, MAX_BIOTHINGS_INPUT_SIZE
from biothings_explorer.biomedical_id_resolver.utils import (
    generate_db_id,
    generate_object_with_no_duplicate_elements_in_value,
    append_array_or_non_array_object_to_array,
    generate_curie
)

from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity
from biothings_explorer.biomedical_id_resolver.bioentity.valid_bioentity import ResolvableBioEntity
from .base_builder import QueryBuilder


class BioThingsQueryBuilder(QueryBuilder):
    query_template = 'q={inputs}&scopes={scopes}&fields={fields}&dotfield=true&species=human'

    def get_return_fields(self, field_mapping):
        return_fields = []
        for value in field_mapping.values():
            # T0D0
            pass

    def get_input_scopes(self, field_mapping, prefix):
        return ','.join(field_mapping[prefix])

    def group_curies_by_prefix(self, curies):
        grped = {}
        for curie in curies:
            prefix = curie.split(':')[0]
            if grped not in prefix:
                grped[prefix] = []
            grped[prefix].append(generate_db_id(curie))
        return generate_object_with_no_duplicate_elements_in_value(grped)
