import unittest
from ..query import APIQueryDispatcher

resolved_ids = {
    "NCBIGene:1017": 'k',
    "CHEBI:1234": 'L'
}

resolved_invalid_ids = {
    "NCBIGene:1017": 'kkkk',
    "CHEBI:1234": 'LLL'
}


class TestQueryClass(unittest.TestCase):
    def test_failed_promise_should_be_excluded_in_the_result(self):
        success = {
            'status': 'fulfilled',
            'value': [{'id': 1}]
        }

        fail = {
            'status': 'rejected',
            'reason': 'bad request'
        }

        caller = APIQueryDispatcher([])
        res = caller._merge([success, fail, fail])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0], success['value'][0])

    def test_successful_promise_should_be_correctly_merged(self):
        success1 = {
            'status': 'fulfilled',
            'value': [{'id': 1}]
        }

        success2 = {
            'status': 'fulfilled',
            'value': [{'id': 3}]
        }

        fail = {
            'status': 'rejected',
            'reason': 'bad request',
        }

        caller = APIQueryDispatcher([])
        res = caller._merge([success1, success2, success1, fail, fail])
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0], success1['value'][0])
        self.assertEqual(res[1], success2['value'][0])
        self.assertEqual(res[2], success1['value'][0])

    def test_logs_is_correctly_populated(self):
        success1 = {
            'status': 'fulfilled',
            'value': [{'id': 1}]
        }

        success2 = {
            'status': 'fulfilled',
            'value': [{'id': 3}]
        }

        fail = {
            'status': 'rejected',
            'reason': 'bad request',
        }

        caller = APIQueryDispatcher([])
        res = caller._merge([success1, success2, success1, fail, fail])
        self.assertEqual(len(caller.logs), 1)
        self.assertIn('message', caller.logs[0])
        self.assertEqual('call-apis: Total number of results returned for this query is 3', caller.logs[0]['message'])

    def test_empty_result_should_return_an_empty_dict(self):
        caller = APIQueryDispatcher([])
        res = caller._group_output_ids_by_semantic_type([])
        self.assertEqual(res, {})

    def test_output_ids_are_correctly_grouped(self):
        caller = APIQueryDispatcher([])
        result = [
            {
                "$edge_metadata": {
                    "output_type": 'Gene'
                },
                "$output": {
                    "original": "NCBIGene:1017"
                }
            },
            {
                "$edge_metadata": {
                    "output_type": 'Gene'
                },
                "$output": {
                    "original": "NCBIGene:1018"
                }
            },
            {
                "$edge_metadata": {
                    "output_type": 'Disease'
                },
                "$output": {
                    "original": "MONDO:1234"
                }
            }
        ]

        res = caller._group_output_ids_by_semantic_type(result)
        self.assertIn('Disease', res)
        self.assertEqual(res['Disease'], ['MONDO:1234'])
        self.assertIn('Gene', res)
        self.assertEqual(res['Gene'], ['NCBIGene:1017', 'NCBIGene:1018'])

    def test_check_if_annotated_ids_are_correctly_mapped(self):
        res = [
            {
                "$edge_metadata": {
                    "output_type": "Gene"
                },
                "$output": {
                    "original": "NCBIGene:1017"
                }
            },
            {
                "$edge_metadata": {
                    "output_type": "ChemicalSubstance"
                },
                "$output": {
                    "original": "CHEBI:1234"
                }
            }
        ]

        caller = APIQueryDispatcher([])
        annotated_result = caller._annotate(res)
        self.assertEqual(len(annotated_result), 2)

    def test_if_set_enabled_equal_to_false_return_the_result_itself(self):
        res = [
            {
                "$edge_metadata": {
                    "output_type": "Gene"
                },
                "$output": {
                    "original": "NCBIGene:1017"
                }
            },
            {
                "$edge_metadata": {
                    "output_type": "ChemicalSubstance"
                },
                "$output": {
                    "original": "CHEBI:1234"
                }
            }
        ]

        caller = APIQueryDispatcher([])
        annotated_result = caller._annotate(res, False)
        self.assertEqual(annotated_result, res)
