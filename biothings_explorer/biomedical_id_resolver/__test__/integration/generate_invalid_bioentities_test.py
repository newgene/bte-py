import unittest
from biothings_explorer.biomedical_id_resolver.fake import generate_invalid
from biothings_explorer.biomedical_id_resolver.bioentity.irresolvable_bioentity import IrresolvableBioEntity


class TestGenerateInvalidFunction(unittest.TestCase):
    def test_invalid_inputs_should_be_generated(self):
        _input = {
            'Gene': ["NCBIGene:1017", "NCBIGene:1018"]
        }

        res = generate_invalid(_input)
        self.assertIn('NCBIGene:1017', res)
        self.assertIn('NCBIGene:1018', res)
        self.assertIsInstance(res['NCBIGene:1017'][0], IrresolvableBioEntity)
