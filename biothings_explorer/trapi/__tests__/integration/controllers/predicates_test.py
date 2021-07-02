import unittest
from functools import reduce
from biothings_explorer.trapi.biothings.controllers.predicates import PredicatesHandler


class TestPredicatesModule(unittest.TestCase):
    def test_load_meta_kg_if_only_smartapi_id_is_provided_should_return_spec_for_that_smartapi_id(self):
        handler = PredicatesHandler()
        res = handler._load_meta_kg('59dce17363dce279d389100834e43648')
        api = list(set(item['association']['api_name'] for item in res.ops))
        self.assertEqual(len(api), 1)
        self.assertEqual(api[0], 'MyGene.info API')

    @unittest.skip
    def test_load_meta_kg_if_invalid_id_is_provided_should_raise_an_error(self):
        handler = PredicatesHandler()
        #self.assertRaises()

    def test_load_meta_kg_if_invalid_smartapi_id_is_provided_smartapi_id_should_take_precedence(self):
        handler = PredicatesHandler()
        res = handler._load_meta_kg('59dce17363dce279d389100834e43648', 'Multiomics Provider')
        api = list(set(item['association']['api_name'] for item in res.ops))
        self.assertEqual(len(api), 1)
        self.assertEqual(api[0], 'MyGene.info API')

    def test_load_meta_kg_if_team_is_provided_should_return_meta_kg_for_all_that_team(self):
        handler = PredicatesHandler()
        res = handler._load_meta_kg(None, 'Multiomics Provider')
        apis = list(set(
           reduce(lambda prev, current: [*prev, *current], [item['association']['x-translator']['team'] for item in res.ops], [])
        ))
        self.assertEqual(len(apis), 2)
        self.assertIn('Multiomics Provider', apis)
        self.assertIn('Service Provider', apis)

    @unittest.skip
    def test_load_meta_kg_if_invalid_team_name_is_provided_should_return_an_empty_list(self):
        handler = PredicatesHandler()

    def test_load_meta_kg_by_default_should_return_all_ops(self):
        handler = PredicatesHandler()
        res = handler._load_meta_kg()
        api = list(set(item['association']['api_name'] for item in res.ops))
        self.assertGreater(len(api), 5)
        self.assertGreater(len(res.ops), 20)


class TestModifyCategoryFunction(unittest.TestCase):
    def test_capitalized_and_biolink_prefixed_category_should_return_itself(self):
        handler = PredicatesHandler()
        res = handler._modify_category('biolink:Disease')
        self.assertEqual(res, 'biolink:Disease')

    def test_biolink_prefixed_but_not_capitalized_category_should_return_the_capitalized_form(self):
        handler = PredicatesHandler()
        res = handler._modify_category('biolink:disease')
        self.assertEqual(res, 'biolink:Disease')

    def test_not_biolink_prefixed_and_not_capitalized_category_should_return_prefixed_and_capitalized_form(self):
        handler = PredicatesHandler()
        res = handler._modify_category('disease')
        self.assertEqual(res, 'biolink:Disease')

    def test_not_biolink_prefixed_but_capitalized_category_should_return_biolink_prefixed_and_capitalized_form(self):
        handler = PredicatesHandler()
        res = handler._modify_category('Disease')
        self.assertEqual(res, 'biolink:Disease')


class TestModifyPredicateFunction(unittest.TestCase):
    def test_snakecased_and_biolink_prefixed_prefix_should_return_itself(self):
        handler = PredicatesHandler()
        res = handler._modify_predicate('biolink:treated_by')
        self.assertEqual(res, 'biolink:treated_by')