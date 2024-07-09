from .trapi_query_builder import TRAPIQueryBuilder
from .template_query_builder import TemplateQueryBuilder
from ..edge import MetaKGEdge


def builder_factory(edge: MetaKGEdge, is_trapi: bool):
    if is_trapi:
        return TRAPIQueryBuilder(edge)
    return TemplateQueryBuilder(edge)
