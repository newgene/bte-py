from abc import ABC


class BioEntity(ABC):
    @property
    def semantic_types(self):
        pass

    @semantic_types.setter
    def semantic_types(self, semantic_types):
        self.semantic_types = semantic_types

    @property
    def primary_id(self):
        pass

    @property
    def label(self):
        pass

    @property
    def curies(self):
        pass

    @property
    def db_ids(self):
        pass

    @property
    def attributes(self):
        pass
