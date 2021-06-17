import unittest
from biothings_explorer.bte_trapi_query_graph_handler.graph.graph import Graph


class Node1:
    def get_id(self):
        return 'qg1'


class Node2:
    def get_id(self):
        return 'qg2'


qg_node1 = Node1()
qg_node2 = Node2()


class TrapiQEdge:
    def is_reversed(self):
        return False
    def get_subject(self):
        return qg_node1
    def get_object(self):
        return qg_node2

trapi_qEdge_obj = TrapiQEdge()
record1 = {
    "$edge_metadata": {
            "trapi_qEdge_obj": trapi_qEdge_obj,
            "api_name": "API1",
            "source": "source1",
            "predicate": "predicate1"
        },
        "publications": ["PMID:1", "PMID:2"],
        "$output": {
            "obj": [
                {
                    "primaryID": "outputPrimaryID"
                }
            ]
        },
        "$input": {
            "obj": [
                {
                    "primaryID": "inputPrimaryID"
                }
            ]
        },
        "relation": "relation1"
}

record2 = {
    "$edge_metadata": {
            "trapi_qEdge_obj": trapi_qEdge_obj,
            "api_name": "API2",
            "source": "source2",
            "predicate": "predicate1"
        },
        "publications": ["PMC:1", "PMC:2"],
        "$output": {
            "obj": [
                {
                    "primaryID": "outputPrimaryID"
                }
            ]
        },
        "$input": {
            "obj": [
                {
                    "primaryID": "inputPrimaryID"
                }
            ]
        },
        "relation": "relation2"
}

record3 = {
    "$edge_metadata": {
            "trapi_qEdge_obj": trapi_qEdge_obj,
            "api_name": "API3",
            "source": "source3",
            "predicate": "predicate2"
        },
        "publications": ["PMC:3", "PMC:4"],
        "$output": {
            "obj": [
                {
                    "primaryID": "outputPrimaryID"
                }
            ]
        },
        "$input": {
            "obj": [
                {
                    "primaryID": "inputPrimaryID"
                }
            ]
        },
        "relation": "relation3"
}


class TestGraph(unittest.TestCase):
    def test_a_single_query_result_is_correctly_updated(self):
        g = Graph()
        g.update([record1])
        self.assertIn('outputPrimaryID-qg2', g.nodes)
        self.assertIn('inputPrimaryID-qg1', g.nodes)
        self.assertEqual(g.nodes['outputPrimaryID-qg2']._primary_id, 'outputPrimaryID')
        self.assertEqual(g.nodes['outputPrimaryID-qg2']._qg_id, 'qg2')
        self.assertEqual([item for item in g.nodes['outputPrimaryID-qg2']._source_nodes], ['inputPrimaryID-qg1'])
        self.assertEqual([item for item in g.nodes['outputPrimaryID-qg2']._source_qg_nodes], ['qg1'])
        self.assertEqual(g.nodes['inputPrimaryID-qg1']._primary_id, 'inputPrimaryID')
        self.assertEqual(g.nodes['inputPrimaryID-qg1']._qg_id, 'qg1')
        self.assertEqual([item for item in g.nodes['inputPrimaryID-qg1']._target_nodes], ['outputPrimaryID-qg2'])
        self.assertEqual([item for item in g.nodes['inputPrimaryID-qg1']._target_qg_nodes], ['qg2'])
        self.assertIn('inputPrimaryID-biolink:predicate1-outputPrimaryID', g.edges)
        self.assertEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].apis], ['API1'])
        self.assertEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].sources], ['source1'])
        # in most cases we would compare lists directly but publications is actually a set so the ordering can be different
        # it's a better choice to compare list count
        self.assertCountEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].publications], ['PMID:1', 'PMID:2'])
        self.assertIn('relation', g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].attributes)
        self.assertEqual(g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].attributes['relation'], 'relation1')

    def test_multiple_query_results_for_same_edge_are_correctly_updated(self):
        g = Graph()
        g.update([record1, record2])
        self.assertIn('outputPrimaryID-qg2', g.nodes)
        self.assertIn('inputPrimaryID-qg1', g.nodes)
        self.assertEqual(g.nodes['outputPrimaryID-qg2']._primary_id, 'outputPrimaryID')
        self.assertEqual(g.nodes['outputPrimaryID-qg2']._qg_id, 'qg2')
        self.assertEqual([item for item in g.nodes['outputPrimaryID-qg2']._source_nodes], ['inputPrimaryID-qg1'])
        self.assertEqual([item for item in g.nodes['outputPrimaryID-qg2']._source_qg_nodes], ['qg1'])
        self.assertEqual('inputPrimaryID', g.nodes['inputPrimaryID-qg1']._primary_id)
        self.assertEqual('qg1', g.nodes['inputPrimaryID-qg1']._qg_id)
        self.assertEqual([item for item in g.nodes['inputPrimaryID-qg1']._target_nodes], ['outputPrimaryID-qg2'])
        self.assertEqual([item for item in g.nodes['inputPrimaryID-qg1']._target_qg_nodes], ['qg2'])
        self.assertIn('inputPrimaryID-biolink:predicate1-outputPrimaryID', g.edges)
        self.assertCountEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].apis], ['API1', 'API2'])
        self.assertCountEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].sources], ['source1', 'source2'])
        self.assertCountEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].publications], ['PMID:1', 'PMID:2', 'PMC:1', 'PMC:2'])
        self.assertIn('relation', g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].attributes)
        self.assertEqual(g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].attributes['relation'], 'relation2')

    def test_multiple_query_results_for_different_edges_are_correctly_updated(self):
        g = Graph()
        g.update([record1, record2, record3])
        self.assertIn('outputPrimaryID-qg2', g.nodes)
        self.assertIn('inputPrimaryID-qg1', g.nodes)
        self.assertEqual(g.nodes['outputPrimaryID-qg2']._primary_id, 'outputPrimaryID')
        self.assertEqual(g.nodes['outputPrimaryID-qg2']._qg_id, 'qg2')
        self.assertEqual([item for item in g.nodes['outputPrimaryID-qg2']._source_nodes], ['inputPrimaryID-qg1'])
        self.assertEqual([item for item in g.nodes['outputPrimaryID-qg2']._source_qg_nodes], ['qg1'])
        self.assertEqual(g.nodes['inputPrimaryID-qg1']._primary_id, 'inputPrimaryID')
        self.assertEqual(g.nodes['inputPrimaryID-qg1']._qg_id, 'qg1')
        self.assertEqual([item for item in g.nodes['inputPrimaryID-qg1']._target_nodes], ['outputPrimaryID-qg2'])
        self.assertEqual([item for item in g.nodes['inputPrimaryID-qg1']._target_qg_nodes], ['qg2'])
        self.assertIn('inputPrimaryID-biolink:predicate1-outputPrimaryID', g.edges)
        self.assertCountEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].apis], ['API1', 'API2'])
        self.assertCountEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].sources], ['source1', 'source2'])
        self.assertCountEqual([item for item in g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].publications], ['PMID:1', 'PMID:2', 'PMC:1', 'PMC:2'])
        self.assertIn('relation', g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].attributes)
        self.assertEqual(g.edges['inputPrimaryID-biolink:predicate1-outputPrimaryID'].attributes['relation'], 'relation2')
        self.assertIn('inputPrimaryID-biolink:predicate2-outputPrimaryID', g.edges)
        self.assertEqual([item for item in g.edges['inputPrimaryID-biolink:predicate2-outputPrimaryID'].apis], ['API3'])
        self.assertEqual([item for item in g.edges['inputPrimaryID-biolink:predicate2-outputPrimaryID'].sources], ['source3'])
        self.assertCountEqual([item for item in g.edges['inputPrimaryID-biolink:predicate2-outputPrimaryID'].publications], ['PMC:3', 'PMC:4'])
        self.assertIn('relation', g.edges['inputPrimaryID-biolink:predicate2-outputPrimaryID'].attributes)
        self.assertEqual(g.edges['inputPrimaryID-biolink:predicate2-outputPrimaryID'].attributes['relation'], 'relation3')