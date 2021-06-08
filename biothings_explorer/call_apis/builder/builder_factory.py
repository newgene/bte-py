from .query_builder import QueryBuilder
from .trapi_query_builder import TRAPIQueryBuilder


def builder_factory(edge):
    if 'tags' in edge and 'bte-trapi' in edge['tags']:
        return TRAPIQueryBuilder(edge)
    return QueryBuilder(edge)
