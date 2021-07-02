import unittest
from biothings_explorer.query_graph_handler.helper import QueryGraphHelper


class Node1:
    def get_id(self):
        return 'n01'

    def get_category(self):
        return 'Node1Type'


class Node2:
    def get_id(self):
        return 'n02'

    def get_category(self):
        return 'Node2Type'


node_object1 = Node1()
node_object2 = Node2()
helper = QueryGraphHelper()


class TestHelperModuler(unittest.TestCase):

    def test_if_edge_is_reversed_should_return_the_node_id_of_the_subject(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return True

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            }
        }
        res = helper._get_input_query_node_id(record)
        self.assertEqual(res, 'n01')

    def test_if_edge_is_not_reversed_should_return_the_node_id_of_the_subject(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return False

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            }
        }
        res = helper._get_input_query_node_id(record)
        self.assertEqual(res, 'n02')

    def test_get_output_query_node_if_edge_is_reversed_should_return_the_node_id_of_the_subject(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return True

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            }
        }
        res = helper._get_output_query_node_id(record)
        self.assertEqual(res, 'n02')

    def test_get_output_query_node_if_edge_is_not_reversed_should_return_the_node_id(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return False

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            }
        }
        res = helper._get_output_query_node_id(record)
        self.assertEqual(res, 'n01')

    def test_get_input_id_if_edge_is_reversed_should_return_the_primary_id_of_the_output(self):
        class Edge:
            def is_reversed(self):
                return True
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output'
                }]
            }
        }
        res = helper._get_input_id(record)
        self.assertEqual(res, 'output')

    def test_get_input_id_if_edge_is_not_reversed_should_return_the_node_id_of_the_subject(self):
        class Edge:
            def is_reversed(self):
                return False
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output'
                }]
            }
        }
        res = helper._get_input_id(record)
        self.assertEqual(res, 'input')

    def test_get_output_id_if_edge_is_reversed_should_return_the_node_id_of_the_subject(self):
        class Edge:
            def is_reversed(self):
                return True
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output'
                }]
            }
        }
        res = helper._get_output_id(record)
        self.assertEqual(res, 'input')

    def test_get_output_id_if_edge_is_not_reversed_should_return_the_node_id_of_the_object(self):
        class Edge:
            def is_reversed(self):
                return False
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output'
                }]
            }
        }
        res = helper._get_output_id(record)
        self.assertEqual(res, 'output')

    def test_get_api_edge_metadata_including_api_name_should_return_the_name(self):
        record = {
            '$edge_metadata': {
                'api_name': 'MyGene.info API'
            }
        }
        res = helper._get_api(record)
        self.assertEqual(res, 'MyGene.info API')

    def test_get_api_edge_metadata_not_including_api_name_should_return_an_empty_string(self):
        record = {
            '$edge_metadata': {
                'api_name1': 'MyGene.info API'
            }
        }
        res = helper._get_api(record)
        self.assertIsNone(res)

    def test_get_source_edge_metadata_including_source_should_return_the_source(self):
        record = {
            '$edge_metadata': {
                'api_name': 'MyGene.info API',
                'source': 'CPDB'
            }
        }
        res = helper._get_source(record)
        self.assertEqual(res, 'CPDB')

    def test_get_source_edge_metadata_not_including_source_should_return_an_empty_string(self):
        record = {
            '$edge_metadata': {
                'api_name1': 'MyGene.info API'
            }
        }
        res = helper._get_source(record)
        self.assertIsNone(res)

    def test_create_unique_edge_id(self):
        class Edge:
            def is_reversed(self):
                return False
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object,
                'api_name': 'MyGene.info API',
                'source': 'CPDB'
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output'
                }]
            }
        }
        res = helper._create_unique_edge_id(record)
        self.assertEqual(res, 'input-output-MyGene.info API-CPDB')

    def test_get_input_category_if_edge_is_reversed_should_return_the_category_of_the_object(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return True

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'semanticType': 'inputType'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'semanticType': 'outputType'
                }]
            }
        }
        res = helper._get_input_category(record)
        self.assertEqual(res, 'outputType')

    def test_get_input_category_if_edge_is_not_reversed_should_return_the_node_id_of_the_subject(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return False

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'semanticType': 'inputType'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'semanticType': 'outputType'
                }]
            }
        }
        res = helper._get_input_category(record)
        self.assertEqual(res, 'inputType')

    def test_get_output_category_if_edge_is_reversed_should_return_the_node_id_of_the_subject(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return True

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'semanticType': 'inputType'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'semanticType': 'outputType'
                }]
            }
        }
        res = helper._get_output_category(record)
        self.assertEqual(res, 'inputType')

    def test_get_output_category_if_edge_is_not_reversed_should_return_the_node_id_of_the_object(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return False

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'semanticType': 'inputType'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'semanticType': 'outputType'
                }]
            }
        }
        res = helper._get_output_category(record)
        self.assertEqual(res, 'outputType')

    def test_get_input_label_if_edge_is_reversed_should_return_the_label_of_the_output(self):
        class Edge:
            def is_reversed(self):
                return True
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel'
                }]
            }
        }
        res = helper._get_input_label(record)
        self.assertEqual(res, 'outputLabel')

    def test_get_input_label_if_edge_is_not_reversed_should_return_the_node_label_of_the_subject(self):
        class Edge:
            def is_reversed(self):
                return False
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel'
                }]
            }
        }
        res = helper._get_input_label(record)
        self.assertEqual(res, 'inputLabel')

    def test_get_output_label_if_edge_is_reversed_should_return_the_label_of_the_subject(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return True

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel'
                }]
            }
        }
        res = helper._get_output_label(record)
        self.assertEqual(res, 'inputLabel')

    def test_get_output_label_if_edge_is_not_reversed_should_return_the_node_id_of_the_object(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return False
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel'
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel'
                }]
            }
        }
        res = helper._get_output_label(record)
        self.assertEqual(res, 'outputLabel')

    def test_get_input_equivalent_identifiers_if_edge_is_reversed_should_return_the_curies_of_the_output(self):
        class Edge:
            def is_reversed(self):
                return True
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel',
                    'curies': ['123', '456']
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel',
                    'curies': ['789']
                }]
            }
        }
        res = helper._get_input_equivalent_ids(record)
        self.assertEqual(res, ['789'])

    def test_get_input_equivalent_identifiers_if_error_occurred_return_none(self):
        class Edge:
            def is_reversed(self):
                raise Exception('')

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': {
                    'primaryID': 'input',
                    'label': 'inputLabel',
                    'curies': ['123', '456']
                }
            },
            '$output': {
                'obj': {
                    'primaryID': 'output',
                    'label': 'outputLabel',
                    'curies': ['789']
                }
            }
        }
        res = helper._get_input_equivalent_ids(record)
        self.assertIsNone(res)

    def test_get_input_equivalent_identifiers_if_edge_is_not_reversed_should_return_the_curies_of_the_subject(self):
        class Edge:
            def is_reversed(self):
                return False

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel',
                    'curies': ['123', '456']
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel',
                    'curies': ['789']
                }]
            }
        }
        res = helper._get_input_equivalent_ids(record)
        self.assertEqual(res, ['123', '456'])

    def test_get_output_equivalent_identifiers_if_edge_is_reversed_should_return_the_curies_of_the_subject(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return True

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel',
                    'curies': ['123', '456']
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel',
                    'curies': ['789']
                }]
            }
        }
        res = helper._get_output_equivalent_ids(record)
        self.assertEqual(res, ['123', '456'])

    def test_get_output_equivalent_identifiers_if_error_occurred_return_none(self):
        class Edge:
            def is_reversed(self):
                raise Exception('')
        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel',
                    'curies': ['123', '456']
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel',
                    'curies': ['789']
                }]
            }
        }
        res = helper._get_output_equivalent_ids(record)
        self.assertIsNone(res, None)

    def test_get_output_equivalent_identifiers_if_edge_is_not_reversed_should_return_the_curies_of_the_object(self):
        class Edge:
            def get_object(self):
                return node_object1

            def get_subject(self):
                return node_object2

            def is_reversed(self):
                return False

        edge_object = Edge()
        record = {
            '$edge_metadata': {
                'trapi_qEdge_obj': edge_object
            },
            '$input': {
                'obj': [{
                    'primaryID': 'input',
                    'label': 'inputLabel',
                    'curies': ['123', '456']
                }]
            },
            '$output': {
                'obj': [{
                    'primaryID': 'output',
                    'label': 'outputLabel',
                    'curies': ['789']
                }]
            }
        }
        res = helper._get_output_equivalent_ids(record)
        self.assertEqual(res, ['789'])

    def test_generate_hash_function(self):
        res = helper._generate_hash('123')
        self.assertEqual(len(res), 32)
        res1 = helper._generate_hash('kkkkkkkkk')
        self.assertEqual(len(res), 32)