import unittest
from biothings_explorer.biomedical_id_resolver.query.scheduler import Scheduler


class TestSchedulerClass(unittest.TestCase):
    def test_promises_with_from_one_api_with_less_than_1000_ids_should_return_one_promise(self):
        scheduler = Scheduler({'Gene': ["NCBIGene:1017"]})
        scheduler.schedule()
        self.assertEqual(len(scheduler.buckets[0]), 1)

    def test_promises_from_multiple_api_with_less_than_1000_ids_should_return_one_promise(self):
        scheduler = Scheduler({"Gene": ["NCBIGene:1017"], "SmallMolecule": ["DRUGBANK:DB0001"]})
        scheduler.schedule()
        self.assertEqual(len(scheduler.buckets[0]), 2)

    def test_promises_from_multiple_api_with_more_than_3000_ids_should_return_one_promise(self):
        fake_ncbi_gene_inputs = ['NCBIGene:' + str(item) for item in range(1990)]
        fake_omim_gene_inputs = ['OMIM:' + str(item) for item in range(2300)]
        fake_drugbank_gene_inputs = ['DRUGBANK:DB00:' + str(item) for item in range(3500)]
        scheduler = Scheduler({'Gene': [*fake_ncbi_gene_inputs, *fake_omim_gene_inputs], 'SmallMolecule': fake_drugbank_gene_inputs})
        scheduler.schedule()
        self.assertEqual(len(scheduler.buckets[0]), 6)
        self.assertEqual(len(scheduler.buckets[1]), 3)
