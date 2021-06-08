
# Welcome to api-response-transform 👋

A python module to transform the JSON output from API into BioLink-compatible JSON structure

## Usage

This package is desgined to be used as a downstream consumer of [@biothings-explorer/smartapi-kg](https://www.npmjs.com/package/@biothings-explorer/smartapi-kg) nodejs package. *@biothings-explorer/smartapi-kg* provides knowledge graph operation info, and when combined with API JSON response, can be consumed as input of the *@biothings-explorer/api-response-transform* package.

- Import

    ```python
    import requests
    from biothings_explorer.api_response_transform.index import Transformer
    ```

- Transform

  - Get API Response

    ```python
    res = requests.post(
        'https://biothings.ncats.io/semmedgene/query',
        params={'q': 'C1332823, C1332824, 123', 'scopes': 'umls'},
        data={'fields': 'name,umls,positively_regulates', 'size': '5'}
    )
    ```

  - Bind with edge info from biothings-explorer/smartapi-kg

    ```python
    _input = {
        'response': res.json(),
        'edge': {
            "input": ["C1332824", "C1332823"],
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
    ```

  - Transform into biolink-compatible format

    ```python
    transformer = Transformer(_input)
    res = transformer.transform()

    # returns [
    #{
    #  "HGNC": '10956',
    #  "pubmed": [ '21685912', '30089514', sequence: true ],
    #  "relation": 'contributes to condition',
    #  "source": [ 'https://archive.monarchinitiative.org/#gwascatalog' ],
    #  "taxid": 'NCBITaxon:9606',
    #  '$reasoner_edge': undefined,
    #  '$association': {
    #    "input_id": 'MONDO',
    #    "input_type": 'Disease',
    #    "output_id": 'HGNC',
    #    "output_type": 'Gene',
    #    "predicate": 'related_to',
    #    "api_name": 'BioLink API',
    #    "smartapi": [Object]
    #  },
    #  '$input': 'MONDO:678',
    #  '$output': 'HGNC:10956',
    #  '$original_input': undefined,
    #  '$input_resolved_identifiers': undefined,
    #  "publications": [ 'PMID:21685912', 'PMID:30089514' ]
    #  },
    #  ...]
    ```

## Run tests

```sh
pytest
```

## Show your support

Give a ⭐️ if this project helped you!
