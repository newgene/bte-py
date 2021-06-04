import unittest
from ..utils import generate_curie, to_array


class TestGenerateCurie(unittest.TestCase):
    def test_if_id_is_a_list(self):
        input_ids = ["1017", "1018"]
        res = generate_curie("NCBIGene", input_ids)
        self.assertEqual('NCBIGene:1017', res)

    def test_if_id_is_not_a_list(self):
        input_ids = '1017'
        res = generate_curie('NCBIGene', input_ids)
        self.assertEqual('NCBIGene:1017', res)

    def test_if_id_is_already_curied(self):
        input_ids = 'NCBIGene1:1017'
        res = generate_curie('NCBIGene', input_ids)
        self.assertEqual('NCBIGene:1017', res)

    def test_if_input_is_already_an_array(self):
        _input = [1]
        res = to_array(_input)
        self.assertEqual(_input, res)

    def test_if_input_is_not_an_array(self):
        _input = 1
        res = to_array(_input)
        self.assertEqual(res, [1])
