import unittest
from biothings_explorer.query_graph_handler.index import TRAPIQueryHandler


class TestTRAPIQueryHandlerGeneralizedQuery(unittest.TestCase):
    OneHopQuery = {
        'nodes': {
            'n0': {
                "ids": ["PUBCHEM.COMPOUND:2662"],
                "categories": ["biolink:SmallMolecule"]
            },
            'n1': {
                "categories": ["biolink:Gene"],
                "ids": ["HGNC:9604"]
            }
        },
        'edges': {
            'e01': {
                'subject': "n0",
                'object': "n1"
            }
        }
    }

    TwoHopQuery = {
        "nodes": {
            "n0": {
                "ids": ["PUBCHEM.COMPOUND:2662"],
                "categories": ["biolink:SmallMolecule"]
            },
            "n1": {
                "categories": ["biolink:Disease"]
            },
            "n2": {
                "categories": ["biolink:Gene"],
                "ids": ["HGNC:9604"]
            }
        },
        "edges": {
            "e0": {
                "subject": "n0",
                "object": "n1"
            },
            "e1": {
                "subject": "n2",
                "object": "n1"
            }
        }
    }

    ThreeHopQuery = {
        "message": {
            "query_graph": {
                "nodes": {
                    "n0": {
                        "ids": ["PUBCHEM.COMPOUND:2662"],
                        "categories": ["biolink:SmallMolecule"]
                    },
                    "n1": {
                        "categories": ["biolink:Disease"]
                    },
                    "n2": {
                        "categories": ["biolink:Pathway"]
                    },
                    "n3": {
                        "categories": ["biolink:Gene"],
                        "ids": ["HGNC:17947"]
                    }
                },
                "edges": {
                    "e0": {
                        "subject": "n0",
                        "object": "n1"
                    },
                    "e1": {
                        "subject": "n1",
                        "object": "n2"
                    },
                    "e2": {
                        "subject": "n2",
                        "object": "n3"
                    }
                }
            }
        }
    }

    BroadCategoryQuery = {
        "message": {
            "query_graph": {
                "nodes": {
                    "n0": {
                         "categories": ["biolink:DiseaseOrPhenotypicFeature"]
                    },
                    "n1": {
                        "ids": ["HGNC:6284"],
                        "categories":["biolink:Gene"]
                    }
                },
                "edges": {
                    "e0": {
                        "subject": "n0",
                        "object": "n1"
                    }
                }
            }
        }
    }

    PredictQuery = {
        "message": {
            "query_graph": {
                "nodes": {
                    "n0": {
                        "ids": ["NCBIGene:3778"],
                        "categories": ["biolink:Gene"]
                    },
                    "n1": {
                        "categories": [
                            "biolink:Disease",
                            "biolink:BiologicalProcess",
                            "biolink:Pathway"
                        ]
                    }
                },
                "edges": {
                    "e01": {
                        "subject": "n0",
                        "object": "n1"
                    }
                }
            }
        }
    }

    @unittest.skip
    def test_query_function_one_hop_has_only_nodes_specified(self):
        query_handler = TRAPIQueryHandler()
        query_handler.set_query_graph(self.OneHopQuery)
        query_handler.query()
        res = query_handler.get_response()
        self.assertEqual(len(res['message']['knowledge_graph']['nodes'].keys()), 2)
        self.assertIn('NCBIGene:5742', res['message']['knowledge_graph']['nodes'])
        self.assertIn('CHEBI:41423', res['message']['knowledge_graph']['nodes'])

    # def test_query_function_two_hop_has_edges_connecting_end_to_end(self):
    #     query_handler = TRAPIQueryHandler()
    #     query_handler.set_query_graph(self.TwoHopQuery)
    #     query_handler.query_2()
    #     res = query_handler.get_response()
    #     self.assertGreater(len(res['message']['knowledge_graph'].keys()), 2)
    #     self.assertIn('NCBIGene:5742', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('CHEBI:41423', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('CHEBI:41423-biolink:treats-MONDO:0018874', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('NCBIGene:5742-biolink:related_to-MONDO:001887', res['message']['knowledge_graph']['nodes'])
    #
    # def test_query_function_three_hop_has_connecting_edges_end_to_end(self):
    #     query_handler = TRAPIQueryHandler()
    #     query_handler.set_query_graph(self.ThreeHopQuery)
    #     query_handler.query_2()
    #     res = query_handler.get_response()
    #     self.assertGreater(len(res['message']['knowledge_graph']['nodes'].keys()), 4)
    #     self.assertIn('NCBIGene:117145', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('REACT:R-HSA-109704', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('MONDO:0018874', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('CHEBI:41423', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('CHEBI:41423-biolink:related_to-MONDO:0002974', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('MONDO:0002974-biolink:related_to-REACT:R-HSA-109704', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('REACT:R-HSA-109704-biolink:has_participant-NCBIGene:117145', res['message']['knowledge_graph']['nodes'])
    #
    # def test_query_function_broad_category_to_known_entity_with_all_entities_present(self):
    #     query_handler = TRAPIQueryHandler()
    #     query_handler.set_query_graph(self.BroadCategoryQuery)
    #     query_handler.query_2()
    #     res = query_handler.get_response()
    #     self.assertIn('NCBIGene:3778', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('MONDO:0005247', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('HP:0002465', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('MONDO:0005247-biolink:related_to-NCBIGene:3778', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('HP:0002465-biolink:related_to-NCBIGene:3778', res['message']['knowledge_graph']['nodes'])
    #
    # def test_query_function_predict_known_entity_to_general_category_to_have_all_nodes_expected(self):
    #     query_handler = TRAPIQueryHandler()
    #     query_handler.set_query_graph(self.PredictQuery)
    #     query_handler.query_2()
    #     res = query_handler.get_response()
    #     self.assertIn('MONDO:0005030', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('NCBIGene:3778', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('GO:0001666', res['message']['knowledge_graph']['nodes'])
    #     self.assertIn('REACT:R-HSA-109582', res['message']['knowledge_graph']['nodes'])
