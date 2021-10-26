import requests
import functools
from biothings_explorer.biomedical_id_resolver.config import APIMETA, TIMEOUT, MAX_BIOTHINGS_INPUT_SIZE
from biothings_explorer.biomedical_id_resolver.utils import (
    generate_db_id,
    generate_object_with_no_duplicate_elements_in_value,
    append_array_or_non_array_object_to_array,
    generate_curie
)

from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity
from biothings_explorer.biomedical_id_resolver.bioentity.valid_bioentity import ResolvableBioEntity
from .base_builder import QueryBuilder


def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


class BioThingsQueryBuilder(QueryBuilder):
    query_template = 'q={inputs}&scopes={scopes}&fields={fields}&dotfield=true&species=human'

    def get_return_fields(self, field_mapping):
        reduced = functools.reduce(lambda prev, current: prev + ','.join(current) + ',', field_mapping.values(), '')
        return reduced

    def get_input_scopes(self, field_mapping, prefix):
        return ','.join(field_mapping[prefix])

    def group_curies_by_prefix(self, curies):
        grped = {}
        for curie in curies:
            prefix = curie.split(':')[0]
            if prefix not in grped:
                grped[prefix] = []
            grped[prefix].append(generate_db_id(curie))
        return generate_object_with_no_duplicate_elements_in_value(grped)

    def get_db_ids_helper(self, records):
        res = {}
        mapping = APIMETA[self.semantic_type]['mapping']
        for prefix in mapping:
            for field_name in mapping[prefix]:
                for record in records:
                    if field_name in record:
                        if prefix not in res:
                            res[prefix] = []
                        res[prefix] = append_array_or_non_array_object_to_array(res[prefix], record[field_name])
        return generate_object_with_no_duplicate_elements_in_value(res)

    def get_attribute_helper(self, records):
        res = {}
        mapping = APIMETA[self.semantic_type].get('additional_attributes_mapping')
        if not mapping:
            return res

        for attr in mapping:
            for field_name in mapping[attr]:
                for record in records:
                    if field_name in record:
                        if attr not in res:
                            res[attr] = []
                        res[attr] = append_array_or_non_array_object_to_array(res[attr], record[field_name])
        return generate_object_with_no_duplicate_elements_in_value(res)

    def group_result_by_query(self, response):
        result = {}
        for rec in response:
            if rec['query'] not in result:
                result[rec['query']] = []
            result[rec['query']].append(rec)
        return result

    def get_db_ids(self, prefix, semantic_type, response):
        result = {}
        grped_response = self.group_result_by_query(response)
        for query in grped_response:
            curie = generate_curie(prefix, query)
            if 'notfound' not in grped_response[query][0]:
                result[curie] = ResolvableBioEntity(
                    semantic_type,
                    self.get_db_ids_helper(grped_response[query]),
                    self.get_attribute_helper(grped_response[query])
                )
            else:
                result[curie] = IrresolvableBioEntity(semantic_type, curie)
        return result

    def build_one_query(self, metadata, prefix, inputs):
        id_return_fields = self.get_return_fields(metadata['mapping'])
        attr_return_fields = ''
        if 'additional_attributes_mapping' in metadata:
            attr_return_fields = self.get_return_fields(metadata['additional_attributes_mapping'])
        return_fields = id_return_fields + attr_return_fields
        scopes = self.get_input_scopes(metadata['mapping'], prefix)
        biothings_query = BioThingsQueryBuilder.query_template\
            .replace('{inputs}', ','.join(inputs))\
            .replace('{scopes}', scopes)\
            .replace('{fields}', return_fields)
        r = requests.post(
            url=metadata['url'],
            timeout=TIMEOUT,
            params={
                'fields': return_fields,
                'dotfield': True,
                'species': 'human'
            },
            json={
                'q': inputs,
                'scopes': scopes
            },
            headers={
                'content-type': 'application/json'
            }
        )

        # try:
        #
        #     data = r.json()
        # except Exception as e:
        #     print(e)
        #     return {}
        data = r.json()
        return self.get_db_ids(prefix, self.semantic_type, data)

    def build_queries(self, metadata, prefix, inputs):
        return [self.build_one_query(metadata, prefix, batch) for batch in chunks(inputs, MAX_BIOTHINGS_INPUT_SIZE)]

    def build(self):
        grped = self.group_curies_by_prefix(self.curies)
        result = []
        reduced = functools.reduce(lambda prev, current: [
            *prev,
            *self.build_queries(self.get_api_metadata(self.semantic_type), current, grped[current])
        ], grped.keys(), [])
        return reduced
