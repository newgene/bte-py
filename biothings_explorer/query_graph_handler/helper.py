import hashlib
from .biolink import BioLinkModelInstance


class QueryGraphHelper:
    def _generate_hash(self, string_to_be_hashed):
        return hashlib.md5(string_to_be_hashed.encode('utf-8')).hexdigest()

    def _get_input_query_node_id(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            return record['$edge_metadata']['trapi_qEdge_obj'].get_object().get_id()
        else:
            return record['$edge_metadata']['trapi_qEdge_obj'].get_subject().get_id()

    def _get_predicate(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            return 'biolink:' + BioLinkModelInstance.reverse(record['$edge_metadata']['predicate'])
        else:
            return 'biolink:' + str(record['$edge_metadata'].get('predicate'))

    def _get_output_query_node_id(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            return record['$edge_metadata']['trapi_qEdge_obj'].get_subject().get_id()
        else:
            return record['$edge_metadata']['trapi_qEdge_obj'].get_object().get_id()

    def _get_output_id(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            if isinstance(record['$input']['obj'][0], dict):
                return record['$input']['obj'][0]['primaryID']
            else:
                return record['$input']['obj'][0].primary_id
        else:
            if isinstance(record['$output']['obj'][0], dict):
                return record['$output']['obj'][0]['primaryID']
            else:
                return record['$output']['obj'][0].primary_id

    def _get_input_id(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            if isinstance(record['$output']['obj'][0], dict):
                return record['$output']['obj'][0]['primaryID']
            else:
                return record['$output']['obj'][0].primary_id
        else:
            if isinstance(record['$input']['obj'][0], dict):
                return record['$input']['obj'][0]['primaryID']
            else:
                return record['$input']['obj'][0].primary_id

    def _get_api(self, record):
        return record['$edge_metadata'].get('api_name') or None

    def _get_infores_curie(self, record):
        if record['$edge_metadata'].get('x-translator'):
            return record['$edge_metadata'].get('x-translator').get('infores')
        return None

    def _get_source(self, record):
        return record['$edge_metadata'].get('source') or None

    def _get_publication(self, record):
        return record.get('publications') or None

    def _get_kg_edge_id(self, record):
        edge_meta_data = [
            self._get_input_id(record),
            self._get_output_id(record),
            self._get_api(record),
            self._get_source(record)
        ]
        return self._generate_hash('-'.join([item if item else '' for item in edge_meta_data]))

    def _get_input_category(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            if isinstance(record['$output']['obj'][0], dict):
                return record['$output']['obj'][0].get('semanticType')
            else:
                return record['$output']['obj'][0].semantic_type
        else:
            if isinstance(record['$input']['obj'][0], dict):
                return record['$input']['obj'][0].get('semanticType')
            else:
                return record['$input']['obj'][0].semantic_type

    def _get_output_category(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            if isinstance(record['$input']['obj'][0], dict):
                return record['$input']['obj'][0].get('semanticType')
            else:
                return record['$input']['obj'][0].semantic_type
        else:
            if isinstance(record['$output']['obj'][0], dict):
                return record['$output']['obj'][0].get('semanticType')
            else:
                return record['$output']['obj'][0].semantic_type

    def _get_output_label(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            if isinstance(record['$input']['obj'][0], dict):
                return record['$input']['obj'][0].get('label')
            else:
                return record['$input']['obj'][0].label
        else:
            if isinstance(record['$output']['obj'][0], dict):
                return record['$output']['obj'][0].get('label')
            else:
                return record['$output']['obj'][0].label

    def _get_input_label(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            if isinstance(record['$output']['obj'][0], dict):
                return record['$output']['obj'][0].get('label')
            else:
                return record['$output']['obj'][0].label
        else:
            if isinstance(record['$input']['obj'][0], dict):
                return record['$input']['obj'][0].get('label')
            else:
                return record['$input']['obj'][0].label

    def _get_input_equivalent_ids(self, record):
        try:
            if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
                if isinstance(record['$output']['obj'][0], dict):
                    return record['$output']['obj'][0].get('curies')
                else:
                    return record['$output']['obj'][0].curies
            else:
                if isinstance(record['$input']['obj'][0], dict):
                    return record['$input']['obj'][0].get('curies')
                else:
                    return record['$input']['obj'][0].curies
        except Exception as e:
            print('_get_input_equivalent_ids', e)
            return None

    def _get_input_names(self, record):
        try:
            if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
                return record['$output']['obj'][0]['dbIDs']['name']
            else:
                return record['$input']['obj'][0]['dbIDs']['name']
        except Exception as e:
            return None

    def _get_output_names(self, record):
        try:
            if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
                return record['$input']['obj'][0]['dbIDs']['name']
            else:
                return record['$output']['obj'][0]['dbIDs']['name']
        except Exception as e:
            return None

    def _get_input_attributes(self, record):
        try:
            if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
                return record['$output']['obj'][0].get('attributes')
            else:
                return record['$input']['obj'][0].get('attributes')
        except Exception as e:
            return None

    def _get_output_equivalent_ids(self, record):
        try:
            if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
                return record['$input']['obj'][0]['curies']
            else:
                return record['$output']['obj'][0]['curies']
        except Exception as e:
            pass

    def _get_output_attributes(self, record):
        if record['$edge_metadata']['trapi_qEdge_obj'].is_reversed():
            if isinstance(record['$input']['obj'][0], dict):
                return record['$input']['obj'][0].get('attributes')
            else:
                return record['$input']['obj'][0].attributes
        else:
            if isinstance(record['$output']['obj'][0], dict):
                return record['$output']['obj'][0].get('attributes')
            else:
                return record['$output']['obj'][0].attributes
