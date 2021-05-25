import unittest
from biothings_explorer.biolink_model.object.slot_object import Slot


class TestSlotObject(unittest.TestCase):
    def test_inverse_property_is_correctly_retreived_if_provided(self):
        s = Slot('negatively_regulates', {'inverse': 'negatively regulated by'})
        self.assertEqual(s.inverse, 'negatively_regulated_by')

    def test_inverse_propert_is_undefined_if_not_provided(self):
        s = Slot('negatively_regulates', {})
        self.assertEqual(s.inverse, None)

    def test_symmetric_property_is_correctly_retreived_if_provided(self):
        s = Slot('correlated_with', {'symmetric': True})
        self.assertEqual(s.symmetric, True)

    def test_symmetric_property_is_false_if_not_provided(self):
        s = Slot('negatively_regulates', {})
        self.assertEqual(s.symmetric, False)

    def test_description_property_is_correctly_retreived_if_provided(self):
        s = Slot('affects_uptake_of', {'description': 'holds between two molecular entities where the action or effect of one impacts the rate of uptake of the other into of a cell, gland, or organ'})
        self.assertEqual(s.description, 'holds between two molecular entities where the action or effect of one impacts the rate of uptake of the other into of a cell, gland, or organ')

    def test_description_property_is_undefined_if_not_provided(self):
        s = Slot('negatively_regulates', {})
        self.assertIsNone(s.description)

    def test_domain_property_is_correctly_retreived_if_provided(self):
        s = Slot('regulates', {'domain': 'physical essence or occurrent'})
        self.assertEqual(s.domain, 'PhysicalEssenceOrOccurrent')

    def test_domain_property_is_undefined_if_not_provided(self):
        s = Slot('negatively_regulates', {})
        self.assertIsNone(s.domain)

    def test_range_property_is_correctly_retreived_if_provided(self):
        s = Slot('regulates', {'range': 'physical essence or occurrent'})
        self.assertEqual(s.range, 'PhysicalEssenceOrOccurrent')

    def test_range_propert_is_undefined_if_not_provided(self):
        s = Slot('negatively_regulates', {})
        self.assertIsNone(s.range)

    def test_exact_mapping_property_is_correctly_retreived_if_provided(self):
        s = Slot('regulates', {'exact_mapping': ["GO:regulates"]})
        self.assertEqual(s.exact_mapping, ["GO:regulates"])

    def test_exact_mapping_property_is_undefined_if_not_provided(self):
        s = Slot('negatively_regulates', {})
        self.assertIsNone(s.exact_mapping, None)

    def test_close_mapping_property_is_correctly_retreived_if_provided(self):
        s = Slot('regulates', {'close_mapping': ["GO:regulated_by", "RO:0002334"]})
        self.assertEqual(s.close_mapping,  ["GO:regulated_by", "RO:0002334"])

    def test_close_mapping_property_is_undefined_if_not_provided(self):
        s = Slot('negatively_regulates', {})
        self.assertIsNone(s.close_mapping)

    def test_narrow_mapping_property_is_correctly_retreived_if_provided(self):
        s = Slot('regulates', {'narrow_mapping': ["WIKIDATA_PROPERTY:P128", "CHEMBL.MECHANISM:modulator"]})
        self.assertEqual(s.narrow_mapping, ["WIKIDATA_PROPERTY:P128", "CHEMBL.MECHANISM:modulator"])

    def test_narrow_mapping_property_is_undefined_if_not_provided(self):
        s = Slot('negatively_regulates', {})
        self.assertIsNone(s.narrow_mapping)

    def test_add_child_function_is_correctly_performed(self):
        s = Slot('regulates', {'narrow_mapping': ["WIKIDATA_PROPERTY:P128", "CHEMBL.MECHANISM:modulator"]})
        s.add_child('negatively regulates')
        self.assertEqual(s.children, ['negatively_regulates'])