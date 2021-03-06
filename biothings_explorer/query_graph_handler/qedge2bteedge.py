from .config import API_LIST
from .log_entry import LogEntry
from .config import API_MAX_ID_LIST
import copy
ID_WITH_PREFIXES = ['MONDO', 'DOID', 'UBERON', 'EFO', 'HP', 'CHEBI', 'CL', 'MGI', 'NCIT']


class QEdge2BTEEdgeHandler:
    def __init__(self, q_edges, kg):
        self.q_edges = q_edges
        self.kg = kg
        self.logs = []

    def set_qedges(self, q_edges):
        self.q_edges = q_edges

    def _find_apis_from_smart_api_edges(self, smartapi_edges):
        return [edge['association']['api_name'] for edge in smartapi_edges]

    def get_smartapi_edges(self, q_edge, kg=None):
        kg = self.kg
        self.logs.append(
            LogEntry(
                'DEBUG',
                None,
                f'BTE is trying to find SmartAPI edges connecting from {q_edge.get_subject().get_categories()}'
                f' to {q_edge.get_object().get_categories()} with predicate {q_edge.get_predicate()}'
            ).get_log()
        )
        filter_criteria = {
            'input_type': q_edge.get_subject().get_categories(),
            'output_type': q_edge.get_object().get_categories(),
            'predicate': q_edge.get_predicate()
        }
        smartapi_edges = kg.filter(filter_criteria)
        for count, item in enumerate(smartapi_edges):
            item['reasoner_edge'] = q_edge
            return item
        if len(smartapi_edges) == 0:
            self.logs.append(LogEntry('Warning', None, f"BTE didn't find any smartapi edges corresponding to {q_edge.get_id()}").get_log())
        else:
            LogEntry(
                'DEBUG',
                None,
                f"BTE found {len(smartapi_edges)} smartapi edges corresponding to {q_edge.get_id()}. These smartaip edges comes from"
                f" {len(set(self._find_apis_from_smart_api_edges(smartapi_edges)))} unique APIs. They are {','.join(list(set(self._find_apis_from_smart_api_edges(smartapi_edges))))}"
            ).get_log()
        return smartapi_edges

    # TODO returns wrong number of edges
    def _create_non_batch_support_bte_edges(self, smartapi_edge):
        bte_edges = []
        input_id = smartapi_edge['association'].get('input_id')
        input_type = smartapi_edge['association'].get('input_type')
        # TODO input_equivalent_identifiers doesn't have correct data
        resolved_ids = smartapi_edge['reasoner_edge'].input_equivalent_identifiers
        for curie in resolved_ids:
            for entity in resolved_ids[curie]:
                if entity.semantic_type == input_type and input_id in entity.db_ids:
                    for _id in entity.db_ids[input_id]:
                        edge = copy.deepcopy(smartapi_edge)
                        edge['input'] = _id
                        edge['input_resolved_identifiers'] = {
                            curie: [entity]
                        }
                        if input_id in ID_WITH_PREFIXES or ':' in str(_id):
                            edge['original_input'] = {
                                _id: curie
                            }
                        else:
                            edge['original_input'] = {
                                input_id + ':' + _id: curie
                            }
                        edge_to_be_pushed = copy.deepcopy(edge)
                        edge_to_be_pushed['resoner_edge'] = smartapi_edge['reasoner_edge']
                        bte_edges.append(edge_to_be_pushed)
        return bte_edges

    # TODO implement chunked loop
    def _create_batch_support_bte_edges(self, smart_api_edge):
        id_mapping = {}
        inputs = []
        bte_edges = []
        input_resolved_identifiers = {}
        input_id = smart_api_edge['association'].get('input_id')
        input_type = smart_api_edge['association'].get('input_type')
        resolved_ids = smart_api_edge['reasoner_edge'].input_equivalent_identifiers
        for curie in resolved_ids:
            for entity in resolved_ids[curie]:
                if 'bte-trapi' in smart_api_edge['tags']:
                    if entity.semantic_type == input_type:
                        input_resolved_identifiers[curie] = [entity]
                        inputs.append(entity.primary_id)
                        id_mapping[entity.primary_id] = curie
                elif entity.semantic_type == input_type and input_id in entity.db_ids:
                    for _id in entity.db_ids[input_id]:
                        if input_id in ID_WITH_PREFIXES or ':' in _id:
                            id_mapping[_id] = curie
                        else:
                            id_mapping[input_id + ':' + _id] = curie
                        input_resolved_identifiers[curie] = [entity]
                        inputs.append(_id)
        chunksize = 10000000
        if 'biothings' in smart_api_edge['tags']:
            chunksize = 1000

        configured_limit = smart_api_edge['query_operation']['batch_size']
        hard_limit = next(filter(lambda api: api['id'] == smart_api_edge['association']['smartapi']['id'] or
                                 api['name'] == smart_api_edge['association']['api_name'], API_MAX_ID_LIST), None)
        chunksize = hard_limit['max'] if hard_limit else configured_limit if configured_limit else chunksize
        if len(id_mapping) > 0:
            edge = copy.deepcopy(smart_api_edge)
            edge['input'] = inputs
            edge['input_resolved_identifiers'] = input_resolved_identifiers
            edge['original_input'] = id_mapping
            edge_to_be_pushed = copy.deepcopy(edge)
            edge_to_be_pushed['reasoner_edge'] = smart_api_edge['reasoner_edge']
            bte_edges.append(edge_to_be_pushed)
        return bte_edges

    def _create_templated_non_batch_support_bte_edges(self, smart_api_edge):
        bte_edges = []
        input_id = smart_api_edge['association']['input_id']
        input_type = smart_api_edge['association']['input_type']
        resolved_ids = smart_api_edge['reasoner_edge']['input_equivalent_identifiers']
        for curie in resolved_ids:
            for entity in resolved_ids[curie]:
                if entity['semantic_type'] == input_type and input_id in entity['db_ids']:
                    for _id in entity['db_ids'][input_id]:
                        edge = copy.deepcopy(smart_api_edge)
                        edge['input'] = {'query_inputs': _id, **edge['query_operation']['templateInputs']}
                        edge['input_resolved_identifiers'] = {
                            curie: [entity]
                        }
                        if input_id in ID_WITH_PREFIXES or ':' in str(_id):
                            edge['original_input'] = {
                                _id: curie
                            }
                        else:
                            edge['original_input'] = {
                                input_id + ':' + _id: curie
                            }
                        edge_to_be_pushed = edge
                        edge_to_be_pushed['reasoner_edge'] = smart_api_edge['reasoner_edge']
                        bte_edges.append(edge_to_be_pushed)
        return bte_edges

    def _create_templated_batch_support_bte_edges(self, smart_api_edge):
        id_mapping = {}
        inputs = []
        bte_edges = []
        input_resolved_identifiers = {}
        input_id = smart_api_edge['association']['input_id']
        input_type = smart_api_edge['association']['input_type']
        resolved_ids = smart_api_edge['reasoner_edge']['input_equivalent_identifiers']
        for curie in resolved_ids:
            for entity in resolved_ids[curie]:
                if 'bte-trapi' in smart_api_edge['tags']:
                    if entity['semantic_type'] == input_type:
                        input_resolved_identifiers[curie] = [entity]
                        inputs.append(entity['primary_id'])
                        id_mapping[entity['primary_id']] = curie
                elif entity['semantic_type'] == input_type and input_id in entity['db_ids']:
                    for _id in entity['db_ids'][input_id]:
                        if input_id in ID_WITH_PREFIXES or ':' in _id:
                            id_mapping[_id] = curie
                        else:
                            id_mapping[input_id + ':' + _id] = curie
                        input_resolved_identifiers[curie] = [entity]
                        inputs.append(_id)
        chunksize = 10000000
        if 'biothings' in smart_api_edge['tags']:
            chunksize = 1000

        configured_limit = smart_api_edge['query_operation']['batch_size']
        hard_limit = next(filter(lambda api: api['id'] == smart_api_edge['association']['smartapi']['id'] or
                                             api['name'] == smart_api_edge['association']['api_name'], API_MAX_ID_LIST),
                          None)
        chunksize = hard_limit['max'] if hard_limit else configured_limit if configured_limit else chunksize
        if len(id_mapping) > 0:
            edge = copy.deepcopy(smart_api_edge)
            edge['input'] = {'query_inputs': inputs, **edge['query_operation']['templateInputs']}
            edge['input_resolved_identifiers'] = input_resolved_identifiers
            edge['original_input'] = id_mapping
            edge_to_be_pushed = copy.deepcopy(edge)
            edge_to_be_pushed['reasoner_edge'] = smart_api_edge['reasoner_edge']
            bte_edges.append(edge_to_be_pushed)
        return bte_edges

    def _create_bte_edges(self, edge):
        support_batch = None
        if isinstance(edge['query_operation'], dict):
            support_batch = edge['query_operation']['support_batch']
        else:
            if hasattr(edge['query_operation'], 'supportBatch'):
                support_batch = edge['query_operation'].supportBatch
            elif hasattr(edge['query_operation'], 'support_batch'):
                support_batch = edge['query_operation'].support_batch
            elif hasattr(edge['query_operation'], '_support_batch'):
                support_batch = edge['query_operation']._support_batch
        use_templating = edge['query_operation']['use_templating']
        if not support_batch:
            if use_templating:
                bte_edges = self._create_templated_non_batch_support_bte_edges(edge)
            else:
                bte_edges = self._create_non_batch_support_bte_edges(edge)
        else:
            if use_templating:
                bte_edges = self._create_templated_batch_support_bte_edges(edge)
            else:
                bte_edges = self._create_batch_support_bte_edges(edge)
        return bte_edges

    # TODO returns wrong bte_edges number on second iteration
    def convert(self, q_edges):
        bte_edges = []
        for edge in q_edges:
            smartapi_edges = self.get_smartapi_edges(edge)
            apis = [api['association']['api_name'] for api in smartapi_edges]
            for item in smartapi_edges:
                # TODO self._create_bte_edges returns wrong amount
                new_edges = self._create_bte_edges(item)
                tmp = []
                for e in new_edges:
                    if hasattr(edge, 'filter'):
                        e['filter'] = edge.filter
                    else:
                        e['filter'] = None
                    tmp.append(e)
                new_edges = tmp
                bte_edges = [*bte_edges, *new_edges]
        if len(bte_edges):
            self.logs.append(
                LogEntry('WARNING', None, "BTE didn't find any bte edges for this batch. Your query terminates.").get_log()
            )
        else:
            self.logs.append(LogEntry('DEBUG', None, f"BTE found {len(bte_edges)} bte edges for this batch.").get_log())
        return bte_edges
