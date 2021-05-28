from biothings_explorer.biomedical_id_resolver.utils import get_prefix_from_curie, generate_db_id
from .base_bioentity import BioEntity


class IrresolvableBioEntity(BioEntity):
    _lead_semantic_type = ''
    _semantic_types = []
    curie = ''

    def __init__(self, semantic_type, curie):
        super(IrresolvableBioEntity, self).__init__()
        self._lead_semantic_type = semantic_type
        self.curie = curie

    @property
    def semantic_types(self):
        if not self._semantic_types:
            return [self._lead_semantic_type]
        return self._semantic_types

    @property
    def semantic_type(self):
        return self._lead_semantic_type

    @semantic_types.setter
    def semantic_types(self, types):
        self._semantic_types = types

    @property
    def primary_id(self):
        return self.curie

    @property
    def label(self):
        return self.curie

    @property
    def curies(self):
        return [self.curie]

    @property
    def db_ids(self):
        return {
            get_prefix_from_curie(self.curie): [self.curie]
        }

    @property
    def attributes(self):
        return {}
