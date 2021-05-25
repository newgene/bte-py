from .base_resolver import BaserResolver
from biothings_explorer.biomedical_id_resolver.query.index import query
from biothings_explorer.biomedical_id_resolver.validate.default_validator import DefaultValidator


class DefaultResolver(BaserResolver):
    def organize_resolved_outputs(self, resolved):
        result = {}
        for recs in resolved:
            for curie in recs.keys():
                if curie not in result:
                    result[curie] = []
                result[curie].append(recs[curie])
        return result

    def resolve(self, usr_input):
        validator = DefaultValidator(usr_input)
        validator.validate()
        query_result = query(validator.resolvable)
        result = self.organize_resolved_outputs(query_result)
        result = self.annotate_unresolved_inputs(validator.irresolvable, result)
        return result
