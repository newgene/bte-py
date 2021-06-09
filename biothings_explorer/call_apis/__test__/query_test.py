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