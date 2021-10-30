from .query_builder import QueryBuilder
from .trapi_query_builder import TRAPIQueryBuilder
from .template_query_builder import TemplateQueryBuilder


def builder_factory(edge):
    if 'tags' in edge and 'bte-trapi' in edge['tags']:
        return TRAPIQueryBuilder(edge)
    elif edge['query_operation'].get('useTemplating'):
        return TemplateQueryBuilder(edge)
    return QueryBuilder(edge)
