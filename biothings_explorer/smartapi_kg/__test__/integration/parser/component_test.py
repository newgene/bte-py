import unittest
import json
from biothings_explorer.smartapi_kg.parser.component import Components


class TestComponent(unittest.TestCase):
    def test_ref_with_trailing_slash(self):
        with open('components.json') as f:
            components = json.load(f)
            cp_obj = Components(components)
            rec = cp_obj.fetch_component_by_ref('#/components/x-bte-kgs-operations/enablesMF/')
            self.assertEqual(rec[0]['source'], 'entrez')

    def test_wrong_ref(self):
        with open('components.json') as f:
            components = json.load(f)
            cp_obj = Components(components)
            rec = cp_obj.fetch_component_by_ref('/components/x-bte-response-mapping')
            self.assertEqual(rec, None)

    def test_wrong_ref_2(self):
        with open('components.json') as f:
            components = json.load(f)
            cp_obj = Components(components)
            rec = cp_obj.fetch_component_by_ref('#/components/x-bte-response-mapping/hello/world')
            self.assertEqual(rec, None)
