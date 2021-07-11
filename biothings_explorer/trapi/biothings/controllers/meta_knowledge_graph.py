import json
import os
from biothings_explorer.smartapi_kg.metakg import MetaKG
from .utils import camel_to_snake


class MetaKnowledgeGraphHandler:
    def __init__(self, smart_API_id=None, team=None):
        self.smart_API_id = smart_API_id
        self.team = team

    def _load_meta_kg(self, smart_API_id=None, team=None):
        smartapi_specs = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'smartapi_specs.json'))

        predicates = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'predicates.json'))

        kg = MetaKG(smartapi_specs, predicates)

        try:
            if smart_API_id:
                kg.construct_MetaKG_sync(False, {'smart_API_id': smart_API_id})
            elif team:
                kg.construct_MetaKG_sync(False, {'team_name': team})
            else:
                kg.construct_MetaKG_sync(True, {})
            if len(kg.ops) == 0:
                raise Exception('Not found - 0 operations')
            return kg
        except Exception as e:
            raise Exception('Failed to load MetaKG')

    def _modify_category(self, category):
        if category.startswith('biolink:'):
            return 'biolink:' + category[8].upper() + category[9:]
        else:
            return 'biolink:' + category[0].upper() + category[1:]

    def _modify_predicate(self, predicate):
        if predicate.startswith('biolink:'):
            return 'biolink:' + camel_to_snake(predicate[8:])
        else:
            return 'biolink:' + camel_to_snake(predicate)

    def get_kg(self, smartapi_id=None, team=None):
        if not smartapi_id:
            smartapi_id = self.smart_API_id
        if not team:
            team = self.team
        kg = self._load_meta_kg(smartapi_id, team)
        knowledge_graph = {
            'nodes': {},
            'edges': []
        }
        predicates = {}
        file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'ids.json'))
        f = open(file_path, )

        # returns JSON object as
        # a dictionary
        ids = json.load(f)
        for semantic_type in ids:
            knowledge_graph['nodes'][self._modify_category(semantic_type)] = {
                'id_prefixes': ids[semantic_type]['id_ranks']
            }
        f.close()
        for op in kg.ops:
            _input = self._modify_category(op['association']['input_type'])
            output = self._modify_category(op['association']['output_type'])
            pred = self._modify_predicate(op['association']['predicate'])
            if _input not in predicates:
                predicates[_input] = {}
            if output not in predicates[_input]:
                predicates[_input][output] = []
            if pred not in predicates[_input][output]:
                predicates[_input][output].append(pred)
        for _input in predicates:
            for output in predicates[_input]:
                for pr in predicates[_input][output]:
                    knowledge_graph['edges'].append({
                        'subject': _input,
                        'predicate': pr,
                        'object': output,
                        'relation': None
                    })
        return knowledge_graph
