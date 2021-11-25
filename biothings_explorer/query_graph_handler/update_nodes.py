import functools
from biothings_explorer.biomedical_id_resolver.resolver import Resolver, resolve_sri


class NodesUpdateHandler:
    def __init__(self, q_edges):
        self.q_edges = q_edges

    def _get_curies(self, q_edges):
        curies = {}
        for edge in q_edges:
            if edge.has_input_resolved():
                return {}
            if edge.has_input():
                input_categories = edge.get_subject().get_categories()
                for category in input_categories:
                    if category not in curies:
                        curies[category] = []
                    curies[category] = [*curies[category], *edge.get_input_curie()]
        return curies

    def _get_equivalent_ids(self, curies):
        # Using biomedical-id-resolver-sri on the latest version
        equivalent_ids = resolve_sri(curies)
        return equivalent_ids

    def set_equivalent_ids(self, q_edges):
        curies = self._get_curies(self.q_edges)
        equivalent_ids = self._get_equivalent_ids(curies)
        for edge in q_edges:
            filtered = [key for key in equivalent_ids.keys() if key in edge.get_input_curie()]
            edge_equivalent_ids = functools.reduce(lambda prev, current: {**prev, **equivalent_ids[current]},
                             filtered, {})
            if len(edge_equivalent_ids) > 0:
                edge['input_equivalent_identifiers'] = edge_equivalent_ids

    def _create_equivalent_ids_object(self, record):
        if record['$output']['obj']:
            return {
                record['$output']['obj']['primaryID']: record['$output']['obj']
            }
        else:
            return

    def update(self, query_result):
        for count, record in enumerate(query_result):
            if query_result[count] and query_result[count]['$output']['obj'][0].primary_id not in query_result[count]['$edge_metadata']['trapi_qEdge_obj'].output_equivalent_identifiers:
                query_result[count]['$edge_metadata']['trapi_qEdge_obj'].output_equivalent_identifiers[query_result[count]['$output']['obj'][0].primary_id] = query_result[count]['$output']['obj']
