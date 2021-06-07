import unittest
import requests
from biothings_explorer.api_response_transform.transformers.semmed_transformer import SemmedTransformer


class TestSemmedTransformer(unittest.TestCase):
    def setUp(self):
        response = requests.post(
            'https://biothings.ncats.io/semmedgene/query',
            params={'q': 'C1332823, C1332824, 123', 'scopes': 'umls'},
            data={'fields': 'name,umls,positively_regulates', 'size': '5'}
        )
        self.api_response = response.json()
        self._input = {
            'response': self.api_response,
            'edge': {
                "input": ["C1332824", "C1332823", "123"],
                "query_operation": {
                    "params": {
                        "fields": "positively_regulates"
                    },
                    "request_body": {
                        "body": {
                            "q": "{inputs[0]}",
                            "scopes": "umls"
                        }
                    },
                    "path": "/query",
                    "path_params": [],
                    "method": "post",
                    "server": "https://biothings.ncats.io/semmedgene",
                    "tags": [
                        "disease",
                        "annotation",
                        "query",
                        "translator",
                        "biothings",
                        "semmed"
                    ],
                    "supportBatch": True,
                    "inputSeparator": ","
                },
                "association": {
                    "input_id": "UMLS",
                    "input_type": "Gene",
                    "output_id": "UMLS",
                    "output_type": "Gene",
                    "predicate": "positively_regulates",
                    "source": "SEMMED",
                    "api_name": "SEMMED Gene API",
                    "smartapi": {
                        "id": "81955d376a10505c1c69cd06dbda3047",
                        "meta": {
                            "ETag": "f94053bc78b3c2f0b97f7afd52d7de2fe083b655e56a53090ad73e12be83673b",
                            "github_username": "kevinxin90",
                            "timestamp": "2020-05-27T16:53:40.804575",
                            "uptime_status": "good",
                            "uptime_ts": "2020-06-12T00:04:31.404599",
                            "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/master/semmed/semmed_gene.yaml"
                        }
                    }
                },
                "response_mapping": {
                    "positively_regulates": {
                        "pmid": "positively_regulates.pmid",
                        "umls": "positively_regulates.umls"
                    }
                },
                "id": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b"
            }
        }

    def test_semmed_pair_input_with_api_response(self):
        tf = SemmedTransformer(self._input)
        res = tf.pair_input_with_api_response()
        self.assertEquals(res["UMLS:C1332823"][0]['umls'], 'C1332823')
        self.assertIn('UMLS:C1332823', res)
        self.assertIsNone(res.get('UMLS:123'))

    def test_wrapper(self):
        tf = SemmedTransformer(self._input)
        res = tf.wrap(self._input['response'][0])
        self.assertIn('positively_regulates', res)

    def test_json_transform(self):
        tf = SemmedTransformer(self._input)
        res = tf.json_transform(self._input['response'][0])
        self.assertEqual(res, self._input['response'][0])

    def test_add_edge_info(self):
        tf = SemmedTransformer(self._input)
        res = tf.pair_input_with_api_response()
        rec = res["UMLS:C1332823"][0]
        rec = tf.wrap(rec)
        result = tf.add_edge_info("UMLS:C1332823", rec["positively_regulates"][0])
        self.assertIn('$edge_metadata', result[0])
        self.assertEquals(result[0]['$edge_metadata']['api_name'], 'SEMMED Gene API')

    def test_main_function_transform(self):
        tf = SemmedTransformer(self._input)
        res = tf.transform()
        self.assertNotIn('UMLS', res[0])
        self.assertNotIn('@type', res[0])
        self.assertIn('$edge_metadata', res[0])
        self.assertIn('$input', res[0])
        self.assertIn('$input', res[-1])
        self.assertGreater(len(res), 30)