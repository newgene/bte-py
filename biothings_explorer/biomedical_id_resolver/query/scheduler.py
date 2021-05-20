import math
from .builder.biothings_builder import BioThingsQueryBuilder
from biothings_explorer.biomedical_id_resolver.config import MAX_CONCURRENT_QUERIES


class Scheduler:
    valid_input = {}
    _buckets = {}

    def __init__(self, valid_input):
        self.valid_input = valid_input
        self._buckets = {}

    @property
    def buckets(self):
        return self._buckets

    def schedule(self):
        for semantic_type in self.valid_input:
            builder = BioThingsQueryBuilder(semantic_type, self.valid_input[semantic_type])
            promises = builder.build()
            for i, p in enumerate(promises):
                bucket_index = math.floor(i / MAX_CONCURRENT_QUERIES)
                if bucket_index not in self._buckets:
                    self._buckets[bucket_index] = []
                self._buckets[bucket_index].append(p)
        return self.buckets
