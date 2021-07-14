import requests
import unittest
from biothings_explorer.api_response_transform.transformers.ctd_transformer import CTDTransformer
from biothings_explorer.api_response_transform.transformers.opentarget_transformer import OpenTargetTransformer
from biothings_explorer.api_response_transform.transformers.biothings_transformer import BioThingsTransformer
from biothings_explorer.api_response_transform.transformers.transformer import BaseTransformer


class TestOpentargetTransformer(unittest.TestCase):
    def setUp(self):
        # TODO can throw urllib3.exceptions.MaxRetryError error
        res = requests.get('https://platform-api.opentargets.io/v3/platform/public/evidence/filter?target=ENSG00000088832&size=100&fields=drug&datasource=chembl')
        self.api_response = res.json()

    def test_opentarget_wrapper(self):
        _input = {
            'response': self.api_response,
            'edge': {
                'input': '238',
                'association': {
                    'output_type': 'Gene'
                },
                'response_mapping': {
                    'sookie': 'kevin'
                }
            }
        }

        tf = OpenTargetTransformer(_input)
        res = tf.wrap(self.api_response)
        self.assertEqual(res['data'][0]['drug']['id'], 'CHEMBL1200686')
        self.assertIn('PIMECROLIMUS', res['data'][0]['drug']['molecule_name'])


class TestCtdTransformer(unittest.TestCase):
    def setUp(self):
        res = requests.get('http://ctdbase.org/tools/batchQuery.go?inputType=chem&inputTerms=D003634|mercury&report=diseases_curated&format=json')
        self.api_response = res.json()

    def test_ctd_wrapper(self):
        _input = {
            'response': self.api_response,
            'edge': {
                'input': '238',
                'association': {
                    'output_type': 'Gene'
                },
                'response_mapping': {
                    'sookie': 'kevin'
                }
            }
        }
        tf = CTDTransformer(_input)
        res = tf.wrap(self.api_response)
        self.assertEqual(res['data'][0]['DiseaseID'], 'D000022')
        self.assertIn('16120699', res['data'][0]['PubMedIDs'])


class TestBiothingsTransformer(unittest.TestCase):
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

    def test_biothings_pair_input_with_api_response(self):
        tf = BioThingsTransformer(self._input)
        res = tf.pair_input_with_api_response()
        self.assertEqual(res["UMLS:C1332823"][0]['umls'], 'C1332823')
        self.assertIn('UMLS:C1332823', res)
        self.assertIsNone(res.get('123'))

    def test_wrapper(self):
        tf = BioThingsTransformer(self._input)
        res = tf.wrap(self._input['response'][0])
        self.assertIn('query', res)
