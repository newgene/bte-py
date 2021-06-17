import unittest
from biothings_explorer.bte_trapi_query_graph_handler.index import TRAPIQueryHandler


class TestTRAPIQueryHandler(unittest.TestCase):
    disease_entity_node = {
        "categories": "Disease",
        "ids": "MONDO:0005737"
    }

    gene_class_node = {
        "categories": "Gene"
    }

    OneHopQuery = {
        "nodes": {
            "n0": disease_entity_node,
            "n1": gene_class_node
        },
        "edges": {
            "e01": {
                "subject": "n0",
                "object": "n1"
            }
        }
    }

    # TODO Fails
    # also the test on the js package fails on due to a network error
    def test_query_with_one_query_edge(self):
        query_handler = TRAPIQueryHandler()
        query_handler.set_query_graph(self.OneHopQuery)
        query_handler.query()
        self.assertIn('nodes', query_handler.knowledge_graph.kg)
