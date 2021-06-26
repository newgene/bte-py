import requests
import json

TYPE_TO_ID_MAPPING = {
    "Gene": "NCBIGene",
    "ChemicalSubstance": "CHEBI",
    "AnatomicalEntity": "UBERON",
    "BiologicalProcess": "GO",
    "MolecularActivity": "GO",
    "Cell": "CL",
    "SequenceVariant": "SO",
    "Disease": "MONDO",
    "PhenotypicFeature": "HP",
}


class NGDFilter:
    def __init__(self, query_result, criteria):
        self.query_result = query_result
        self.criteria = criteria

    def extract_input_id(self, resolved_ids, semantic_type):
        if not resolved_ids:
            return None
        if semantic_type not in TYPE_TO_ID_MAPPING:
            return None
        if 'db_ids' not in resolved_ids:
            return None
        prefix = TYPE_TO_ID_MAPPING[semantic_type]
        if prefix not in resolved_ids['db_ids']:
            return None
        return resolved_ids['db_ids'][prefix][0]

    def query_ngd(self, inputs):
        result = []
        for i in range(0, len(inputs), 1000):
            query = {
                "q": [item.split('-') for item in inputs[i: i + 1000]],
                "scopes": [["subject.id", "object.id"], ["object.id", "subject.id"]],
                "fields": "association.ngd",
                "dotfield": True
            }
            tmp = requests.post('https://biothings.ncats.io/text_mining_co_occurrence_kp/query',
                              data=json.dumps(query),
                              headers={
                                  'Content-Type': 'application/json'
                              })
            data = tmp.json()
            result = [*result, *data]
        return result

    def parse_response(self, res):
        result = {}
        for rec in res:
            if 'association.ngd' in rec:
                result['-'.join(rec['query'])] = rec['association.ngd']
        return result

    def annotate_ngd(self):
        ngd_inputs = set()
        id_dict = {}
        if isinstance(self.query_result, list) and len(self.query_result) > 0:
            for i, rec in enumerate(self.query_result):
                if '$association' in rec:
                    input_type = rec['$association']['input_type']
                    output_type = rec['$association']['output_type']
                    input_resolved_ids = rec['$input_resolved_identifiers'][rec['$original_input'][rec['$input']]]
                    if 'resolved' not in rec['$output_id_mapping']:
                        return
                    output_resolved_ids = rec['$output_id_mapping']['resolved']
                    input_id = self.extract_input_id(input_resolved_ids, input_type)
                    output_id = self.extract_input_id(output_resolved_ids, output_type)
                    if input_id and output_id:
                        s_id = str(input_id)
                        o_id = str(output_id)
                        if input_id == 'Gene':
                            s_id = 'NCBIGene:' + s_id
                        if output_type == 'Gene':
                            o_id = 'NCBIGene:' + o_id
                        ngd_inputs.add(s_id + '-' + o_id)
                        id_dict[i] = s_id + '-' + o_id
                ngd_results = self.query_ngd(list(ngd_inputs))
                parsed_ngd_results = self.parse_response(ngd_results)
                for i, rec in enumerate(self.query_result):
                    if i in id_dict:
                        rec['$ngd'] = parsed_ngd_results[id_dict[i]]
