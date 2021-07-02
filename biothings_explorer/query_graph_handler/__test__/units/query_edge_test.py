import unittest
from biothings_explorer.query_graph_handler.query_edge import QEdge


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

    def test_none_predicate_should_return_itself(self):
        edge = QEdge('e01', {})
        res = edge.get_predicate()
        self.assertIsNone(res)

    def test_an_array_of_non_none_predicates_should_return_itself(self):
        class Curie:
            def get_curie(self):
                return None

        class Subject:
            def get_curie(self):
                return 'yes'

        curie = Curie()
        subject = Subject()

        edge = QEdge('e01', {
            'predicates': ['biolink:treats', 'biolink:targets'],
            'object': curie,
            'subject': subject
        })
        res = edge.get_predicate()
        self.assertIn('treats', res)
        self.assertIn('targets', res)

    def test_an_array_of_non_none_predicates_with_reverse_edge_should_exclude_return_value_if_none(self):
        class Curie:
            def get_curie(self):
                return 'yes'

        class Subject:
            def get_curie(self):
                return None

        curie = Curie()
        subject = Subject()

        edge = QEdge('e01', {
            'predicates': ['biolink:treats', 'biolink:targets'],
            'object': curie,
            'subject': subject
        })
        res = edge.get_predicate()
        self.assertIn('treated_by', res)

    def test_an_array_of_non_none_predicates_with_reverse_edge_should_return_reversed_predicates_if_not_none(self):
        class Curie:
            def get_curie(self):
                return 'yes'

        class Subject:
            def get_curie(self):
                return None

        curie = Curie()
        subject = Subject()

        edge = QEdge('e01', {
            'predicates': ['biolink:treats', 'biolink:targets'],
            'object': curie,
            'subject': subject,
        })
        res = edge.get_predicate()
        self.assertIn('treated_by', res)

    def test_get_output_node_reversed_edge_should_return_the_subject(self):
        class Curie:
            def get_curie(self):
                return 'yes'
            def id(self):
                return 1

        class Subject:
            def get_curie(self):
                return None
            def id(self):
                return 2

        curie = Curie()
        subject = Subject()

        edge = QEdge('e01', {
            'predicates': ['biolink:treats', 'biolink:targets'],
            'object': curie,
            'subject': subject
        })

        res = edge.get_output_node()
        self.assertEqual(res.id(), 2)

    def test_get_output_node_edge_should_return_the_object(self):
        class Curie:
            def get_curie(self):
                return None
            def id(self):
                return 1

        class Subject:
            def get_curie(self):
                return 'aa'
            def id(self):
                return 2

        curie = Curie()
        subject = Subject()
        edge = QEdge('e01', {
            'predicates': ['biolink:treats', 'biolink:targets'],
            'object': curie,
            'subject': subject
        })
        res = edge.get_output_node()
        self.assertEqual(res.id(), 1)
