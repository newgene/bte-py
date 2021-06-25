import os
import re
from biothings_explorer.smartapi_kg.metakg import MetaKG


def camel_to_snake(name):
  name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class PredicatesHandler:
    def __init__(self, smartapi_id=None, team=None):
        self.smartapi_id = smartapi_id
        self.team = team

    def _load_meta_kg(self, smartapi_id=None, team=None):
        smartapi_specs = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'smartapi_specs.json'))

        predicates = os.path.abspath(
            os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'data', 'predicates.json'))

        kg = MetaKG(smartapi_specs, predicates)
        try:
            if smartapi_id is not None:
                kg.construct_MetaKG_sync(False, {'smart_API_id': smartapi_id})
            elif team is not None:
                kg.construct_MetaKG_sync(False, {'team_name': team})
            else:
                kg.construct_MetaKG_sync(True, {})
            if len(kg.ops) == 0:
                raise Exception('Failed to Load MetaKG')
            return kg
        except Exception as e:
            raise Exception('Failed to Load MetaKG')

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

    def get_predicates(self, smartapi_id=None, team=None):
        smartapi_id = self.smartapi_id
        team = self.team
        kg = self._load_meta_kg(smartapi_id, team)
        predicates = {}
        for op in kg.ops:
            _input = self._modify_category(op['association']['input_type'])
            output = self._modify_category(op['association']['output_type'])
            pred = self._modify_predicate(op['association']['predicate'])
            if _input not in predicates:
                predicates[_input] = {}
            if output not in predicates[_input]:
                predicates[_input][output] = []
            if pred not in predicates[_input][output]:
                predicates[_input][output].append = pred
        return predicates
