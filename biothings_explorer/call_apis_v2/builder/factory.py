from .trapi_query_builder import TRAPIQueryBuilder
from .template_query_builder import TemplateQueryBuilder


def builder_factory(edge, is_trapi):
    if is_trapi:
        return TRAPIQueryBuilder(edge)
    return TemplateQueryBuilder(edge)
