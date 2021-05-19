from biothings_explorer.biomedical_id_resolver.config import APIMETA, CURIE
from .base_bioentity import BioEntity


class ResolvableBioEntity(BioEntity):
    _leaf_semantic_type = ''
    _semantic_types = []
    _db_ids = {}
    _attributes = {}

    def __init__(self, semantic_type, db_ids, attributes):
        super(ResolvableBioEntity, self).__init__(self)
        self._leaf_semantic_type = semantic_type
        self._db_ids = db_ids
        self._attributes = attributes

    def get_curie_from_val(self, val, prefix):
        if prefix in CURIE['ALWAYS_PREFIXED']:
            return val
        return prefix + ':' + val

    @property
    def semantic_types(self):
        if not self._semantic_types:
            return [self._leaf_semantic_type]
        return self._semantic_types

    @property
    def semantic_type(self):
        return self._leaf_semantic_type

    @semantic_types.setter
    def semantic_types(self, types):
        self._semantic_types = types

    @property
    def primary_id(self):
        ranks = APIMETA[self._leaf_semantic_type]['id_ranks']
        for prefix in ranks:
            if prefix in self._db_ids:
                return self.get_curie_from_val(self._db_ids[prefix][0], prefix)
        return None

    @property
    def label(self):
        if 'SYMBOL' in self._db_ids:
            return self._db_ids['SYMBOL'][0]
        if 'name' in self._db_ids:
            return self._db_ids['name'][0]
        return self.primary_id

    @property
    def curies(self):
        res = []
        for prefix in self._db_ids:
            for _id in self._db_ids[prefix]:
                res.append(self.get_curie_from_val(_id, prefix))
        return res

    @property
    def db_ids(self):
        return self._db_ids

    @property
    def attributes(self):
        return self._attributes
