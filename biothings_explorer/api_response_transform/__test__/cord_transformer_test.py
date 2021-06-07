import unittest
import requests
from biothings_explorer.api_response_transform.transformers.cord_transformer import CordTransformer


class TestCordTransformer(unittest.TestCase):
    def setUp(self):
        response = requests.post(
            'https://biothings.ncats.io/cord_gene/query',
            params={'q': '238, 239, 240', 'scopes': 'hgnc'},
            data={'fields': 'associated_with'}
        )
        self.api_response = response.json()
        self._input = {
            'response': self.api_response,
            'edge': {
                "input": ["238", "239", "240"],
                "query_operation": {
                    "params": {
                        "fields": "associated_with"
                    },
                    "request_body": {
                        "body": {
                            "q": "{inputs[0]}",
                            "scopes": "hgnc"
                        },
                        "header": "application/x-www-form-urlencoded"
                    },
                    "path": "/query",
                    "path_params": [],
                    "method": "post",
                    "server": "https://biothings.ncats.io/cord_gene",
                    "tags": [
                        "gene",
                        "annotation",
                        "query",
                        "translator",
                        "biothings"
                    ],
                    "supportBatch": True,
                    "inputSeparator": ","
                },
                "association": {
                    "input_id": "HGNC",
                    "input_type": "Gene",
                    "output_id": "HGNC",
                    "output_type": "Gene",
                    "predicate": "related_to",
                    "source": "Translator Text Mining Provider",
                    "api_name": "CORD Gene API",
                    "smartapi": {
                        "id": "6bc54230a6fa7693b2cd113430387ca7",
                        "meta": {
                            "ETag": "5e7512d15d24b57b52cb15604aaa6c24192f48ef00da9732f23aab3707b2061b",
                            "github_username": "kevinxin90",
                            "timestamp": "2020-04-29T00:00:40.725359",
                            "uptime_status": "good",
                            "uptime_ts": "2020-06-12T00:05:25.251375",
                            "url": "https://raw.githubusercontent.com/NCATS-Tangerine/translator-api-registry/master/cord/cord_gene.yml"
                        }
                    }
                },
                "response_mapping": {
                    "related_to": {
                        "HGNC": "associated_with.hgnc",
                        "pmc": "associated_with.pmc"
                    }
                },
                "id": "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b"
            }
        }

    def test_cord_pair_input_with_api_response(self):
        tf = CordTransformer(self._input)
        res = tf.pair_input_with_api_response()
        self.assertIn('HGNC:240', res)
        self.assertIsNone(res.get('HGNC:239'))

    def test_wrapper(self):
        tf = CordTransformer(self._input)
        res = tf.wrap(self._input['response'][0])
        self.assertIn('related_to', res)
        self.assertEqual(res['related_to'][0]['@type'], 'Gene')

    def test_json_transform(self):
        tf = CordTransformer(self._input)
        res = tf.json_transform(self._input['response'][0])
        self.assertEqual(res, self._input['response'][0])

    def test_add_edge_info(self):
        tf = CordTransformer(self._input)
        res = tf.pair_input_with_api_response()
        rec = res['HGNC:238'][0]
        rec = tf.wrap(rec)
        result = tf.add_edge_info("HGNC:238", rec["related_to"][0])
        self.assertIn('$edge_metadata', result[0])
        self.assertEqual(result[0]['$edge_metadata']['api_name'], 'CORD Gene API')

    def test_main_function_transform(self):
        tf = CordTransformer(self._input)
        res = tf.transform()
        self.assertNotIn('HGNC', res[0])
        self.assertIn('$edge_metadata', res[0])
        self.assertIn('$input', res[0])
        self.assertGreater(len(res), 20)
