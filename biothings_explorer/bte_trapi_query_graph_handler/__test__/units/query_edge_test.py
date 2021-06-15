import unittest
from biothings_explorer.bte_trapi_query_graph_handler.query_edge import QEdge


class TestQEdgeClass(unittest.TestCase):
    def test_get_predicate_non_reversed_edge_should_return_predicates_itself(self):
        class Curie:
            def get_curie(self):
                return None

        class Subject:
            def get_curie(self):
                return 'uye'

        curie = Curie()
        subject = Subject()

        edge = QEdge('e01', {
            'predicates': 'biolink:treats',
            'object': curie,
            'subject': subject
        })
        res = edge.get_predicate()
        self.assertIn('treats', res)
