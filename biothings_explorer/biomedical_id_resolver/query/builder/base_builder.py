from abc import ABC
from biothings_explorer.biomedical_id_resolver.config import APIMETA


class QueryBuilder(ABC):
    semantic_type = ''
    curies = []

    def __init__(self, semantic_type, curies):
        self.semantic_type = semantic_type
        self.curies = curies

    def get_api_metadata(self, semantic_type):
        return APIMETA[semantic_type or self.semantic_type]

    def build_queries(self, metadata, prefix, inputs):
        pass

    def build_one_query(self, metadata, prefix, curies):
        pass
