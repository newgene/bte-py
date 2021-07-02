import unittest
from biothings_explorer.query_graph_handler.query_node import QNode
from biothings_explorer.query_graph_handler.query_edge import QEdge
from biothings_explorer.query_graph_handler.query_execution_edge import QExeEdge
from biothings_explorer.query_graph_handler.batch_edge_query import BatchEdgeQueryHandler
from biothings_explorer.smartapi_kg.metakg import MetaKG


class TestBatchEdgeQueryHandler(unittest.TestCase):
    kg = MetaKG()
    kg.construct_MetaKG_sync()

    def test_query_function_subscribe_and_unsubscribe_function(self):
        batch_handler = BatchEdgeQueryHandler(self.kg)
        batch_handler.subscribe(1)
        batch_handler.subscribe(2)
        batch_handler.subscribe(3)
        self.assertIn(2, batch_handler.subscribers)
        batch_handler.unsubscribe(2)
        self.assertNotIn(2, batch_handler.subscribers)
