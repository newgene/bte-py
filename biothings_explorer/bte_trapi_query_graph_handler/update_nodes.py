import functools
from biothings_explorer.biomedical_id_resolver.resolver import Resolver


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
        resolver = Resolver('biolink')
        equivalent_ids = resolver.resolve(curies)
        return equivalent_ids

    def set_equivalent_ids(self, q_edges):
        curies = self._get_curies(self.q_edges)
        if len(curies) == 0:
            for edge in q_edges:
                edge['input_equivalent_identifiers'] = edge['prev_edge']['output_equivalent_identifiers']
            return
        equivalent_ids = self._get_equivalent_ids(curies)
        for edge in q_edges:
            edge_equivalent_ids = functools.reduce(lambda res, key: {**res, key: equivalent_ids[key]}, [key for key in equivalent_ids if key in edge.get_input_curie()], {})
            if len(edge_equivalent_ids) > 0:
                edge['input_equivalent_identifiers'] = edge_equivalent_ids
        return

    def _create_equivalent_ids_object(self, record):
        if record['$output']['obj']:
            return {
                record['$output']['obj']['primaryID']: record['$output']['obj']
            }
        else:
            return

    def update(self, query_result):
        for record in query_result:
            if record['$output']['obj'][0]['primaryID'] not in record['$edge_metadata']['trapi_qEdge_obj']['output_equivalent_identifiers']:
                record['$edge_metadata']['trapi_qEdge_obj']['output_equivalent_identifiers'][record['$output']['obj'][0]['primaryID']] = record['$output']['obj']
    