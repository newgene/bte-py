import unittest
from biothings_explorer.query_graph_handler.query_node import QNode
from biothings_explorer.query_graph_handler.query_edge import QEdge
from biothings_explorer.query_graph_handler.graph.knowledge_graph import KnowledgeGraph


class TestingKnowledgeGraph(unittest.TestCase):
    node_input = {
        "id": "PUBCHEM.COMPOUND:2662-n0",
        "_primaryID": "PUBCHEM.COMPOUND:2662",
        "_qgID": "n0",
        "_curies": [
            "PUBCHEM.COMPOUND:2662",
            "CHEMBL.COMPOUND:CHEMBL118",
            "UNII:JCX84Q7J1L",
            "CHEBI:41423",
            "DRUGBANK:DB00482",
            "MESH:C105934",
            "MESH:D000068579",
            "CAS:169590-42-5",
            "CAS:184007-95-2",
            "CAS:194044-54-7",
            "DrugCentral:568",
            "GTOPDB:2892",
            "HMDB:HMDB0005014",
            "KEGG.COMPOUND:C07589",
            "INCHIKEY:RZEKVGVHFLEQIL-UHFFFAOYSA-N"
        ],
        "_names": [
            "Celecoxib",
            "CELECOXIB",
            "celecoxib",
            "[OBSOLETE] celecoxib"
        ],
        "_semanticType": "SmallMolecule",
        "_nodeAttributes": {},
        "_label": "Celecoxib",
        "_sourceNodes": {},
        "_targetNodes": {},
        "_sourceQGNodes": {},
        "_targetQGNodes": {}
    }

    trapi_edge_input = {
                "id": 'PUBCHEM.COMPOUND:2662-biolink:activity_decreased_by-NCBIGene:771',
                "predicate": 'biolink:activity_decreased_by',
                "subject": 'PUBCHEM.COMPOUND:2662',
                "object": 'NCBIGene:771',
                "apis": set(),
                "sources": set(),
                "publications": set(),
                "inforesCuries": set(),
                "attributes": {
                    "attributes": [
                    {
                        "attribute_type_id": 'biolink:Attribute',
                        "value": 'Ki',
                        "value_type_id": 'EDAM:data_0006',
                        "original_attribute_name": 'affinity_parameter',
                        "value_url": None,
                        "attribute_source": None,
                        "description": None,
                    },
                    {
                        "attribute_type_id": 'biolink:knowledge_source',
                        "value": ['PHAROS_1_norm_edges.jsonl'],
                        "value_type_id": 'EDAM:data_0006',
                        "original_attribute_name": 'knowledge_source',
                        "value_url": None,
                        "attribute_source": None,
                        "description": None,
                    },
                    {
                        "attribute_type_id": 'biolink:aggregator_knowledge_source',
                        "value": ['infores:pharos'],
                        "value_type_id": 'biolink:InformationResource',
                        "original_attribute_name": 'biolink:aggregator_knowledge_source',
                        "value_url": None,
                        "attribute_source": None,
                        "description": None,
                    },
                    {
                        "attribute_type_id": 'biolink:Attribute',
                        "value": 7.75,
                        "value_type_id": 'EDAM:data_0006',
                        "original_attribute_name": 'affinity',
                        "value_url": None,
                        "attribute_source": None,
                        "description": None,
                    },
                    {
                        "attribute_type_id": 'biolink:publications',
                        "value": [
                            'PMID:20605094',
                            'PMID:21852133',
                            'PMID:16290146',
                            'PMID:23965175',
                            'PMID:23965175',
                            'PMID:24513184',
                            'PMID:25766630',
                            'PMID:23067387',
                        ],
                        "value_type_id": 'EDAM:data_0006',
                        "original_attribute_name": 'publications',
                        "value_url": None,
                        "attribute_source": None,
                        "description": None,
                    },
                    {
                        "attribute_type_id": 'biolink:relation',
                        "value": 'GAMMA:ki',
                        "value_type_id": 'EDAM:data_0006',
                        "original_attribute_name": 'relation',
                        "value_url": None,
                        "attribute_source": None,
                        "description": None,
                    },
                    {
                        "attribute_type_id": 'biolink:aggregator_knowledge_source',
                        "value": 'infores:automat.pharos',
                        "value_type_id": 'biolink:InformationResource',
                        "original_attribute_name": 'biolink:aggregator_knowledge_source',
                        "value_url": None,
                        "attribute_source": None,
                        "description": None,
                    },
                ],
        },
    }

    def test_create_node_function_creating_node(self):
        kg = KnowledgeGraph()
        res = kg._create_node(self.node_input)
        self.assertIn('name', res)
        self.assertEqual(res['name'], 'Celecoxib')
        self.assertIn(res, 'categories')
        self.assertEqual(res['categories'][0], 'biolink:SmallMolecule')
        self.assertIn('attributes', res)

    def test_create_attributes_function_edge_attributes(self):
        kg = KnowledgeGraph()
        res = kg._create_attributes(self.trapi_edge_input)
        self.assertEqual(len(res), 0)
        for res_obj in res:
            self.assertIn('attribute_type_id', res_obj)
            self.assertIn('value', res_obj)
            self.assertIn('value_type_id', res_obj)

    def test_create_edge_function_creating_edge(self):
        kg = KnowledgeGraph()
        res = kg._create_edge(self.trapi_edge_input)
        self.assertIn('predicate', res)
        self.assertEqual(res['predicate'], 'biolink:activity_decreased_by')
        self.assertIn('subject', res)
        self.assertEqual(res['subject'], 'PUBCHEM.COMPOUND:2662')
        self.assertIn('object', res)
        self.assertEqual(res['object'], 'NCBIGene:771')
        self.assertIn('attributes', res)
        for res_obj in res['attributes']:
            self.assertIn('attribute_type_id', res_obj)
            self.assertIn('value', res_obj)
            self.assertIn('value_type_id', res_obj)
