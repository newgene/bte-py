from .base_resolver import BaserResolver
from biothings_explorer.biomedical_id_resolver.validate.biolink_based_validator import BioLinkBasedValidator
from biothings_explorer.biomedical_id_resolver.query.index import query
from ..biolink import BioLinkHandlerInstance


class BioLinkBasedResolver(BaserResolver):
    _biolink = BioLinkHandlerInstance

    def __init__(self):
        super(BioLinkBasedResolver, self).__init__()
        self._biolink = BioLinkHandlerInstance

    def construct_prefix_type_dict(self, _input):
        res = {}
        for _type in _input:
            for curie in _input[_type]:
                if curie not in res:
                    res[curie] = []
                if _type not in res[curie]:
                    res[curie].append(_type)
        return res

    def get_path(self, downstream_type, upstream_types):
        paths = [*upstream_types]
        for _type in upstream_types:
            path = [entity.name for entity in self._biolink.class_tree.get_path(downstream_type, _type)]
            paths = [*paths, *path]
        paths.append(downstream_type)
        return [item for item in set(paths)]

    def organize_resolved_outputs(self, resolved, resolvable):
        result = {}
        prefix_type_dict = self.construct_prefix_type_dict(resolvable)
        for recs in resolved:
            for curie in recs.keys():
                if curie not in result:
                    result[curie] = []
                recs[curie].semantic_types = self.get_path(recs[curie].semantic_type, prefix_type_dict[curie])
                result[curie].append(recs[curie])
        return result

    def resolve(self, usr_input):
        validator = BioLinkBasedValidator(usr_input)
        validator.validate()
        query_result = query(validator.resolvable)
        result = self.organize_resolved_outputs(query_result, validator.valid)
        result = self.annotate_unresolved_inputs(validator.irresolvable, result)
        return result
