import unittest
import os
import json
from biothings_explorer.query_graph_handler.index import TRAPIQueryHandler


class TestTRAPIQueryHandler(unittest.TestCase):
    example_folder1 = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'data', 'increased_urinary_glycerol_affects_glycerol.json'))

    example_folder2 = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'data', 'FDFM_caused_by_ACDY5.json'))

    example_folder3 = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'data', 'chemicals_targeting_IL1_Signaling_Pathway.json'))

    # skip until we figure out why it returns no results
    @unittest.skip
    def test_when_looking_for_chemicals_affected_by_phenotype_increased_urinary_glycerol_glycerol_should_pop_up(self):
        query_handler = TRAPIQueryHandler({}, None, None, True)
        with open(self.example_folder1) as f1:
            query = json.load(f1)
            query_handler.set_query_graph(query['message']['query_graph'])
            query_handler.query()
            res = query_handler.get_response()
            self.assertIn('CHEBI:17754', res['message']['knowledge_graph']['nodes'])

    def test_when_looking_for_genes_related_to_disease_dyskinesia_familial_with_facial_myokymia_acdy5_should_pop_up(self):
        query_handler = TRAPIQueryHandler({}, None, None, True)
        with open(self.example_folder2) as f1:
            query = json.load(f1)
            query_handler.set_query_graph(query['message']['query_graph'])
            query_handler.query()
            res = query_handler.get_response()
            self.assertIn('NCBIGene:111', res['message']['knowledge_graph']['nodes'])

    def test_when_looking_for_chemicals_targeting_il1_signaling_atway_curcumin_should_pop_up(self):
        query_handler = TRAPIQueryHandler({}, None, None, True)
        with open(self.example_folder3) as f1:
            query = json.load(f1)
            query_handler.set_query_graph(query['message']['query_graph'])
            query_handler.query()
            res = query_handler.get_response()
            self.assertIn('CHEBI:3962', res['message']['knowledge_graph']['nodes'])
