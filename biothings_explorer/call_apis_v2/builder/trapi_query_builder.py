import json

from ..edge import MetaKGEdge, EdgeQueryOperation


class TRAPIQueryBuilder:
    def __init__(self, edge: MetaKGEdge):
        self.start = 0
        self.has_next = False
        self.edge = edge

    @property
    def query_operation(self) -> EdgeQueryOperation:
        return self.edge.query_operation

    def _get_url(self, _input: str) -> str:
        server = self.query_operation.server
        if server.endswith("/"):
            server = server[: len(server) - 1]

        path = self.query_operation.path

        if isinstance(self.query_operation.path_params, list):
            for param in self.query_operation.path_params:
                val = self.query_operation.path_params[param]
                path = path.replace("{" + param + "}", val).replace(
                    "{inputs[0]}", _input
                )
        return server + path

    def _get_input(self) -> str:
        return self.edge.input

    def _get_request_body(self, _input: str) -> dict:
        qg = {
            "message": {
                "query_graph": {
                    "nodes": {
                        "n0": {
                            "ids": _input if isinstance(_input, list) else [_input],
                            "categories": [
                                "biolink:" + self.edge.association_input_type
                            ],
                        },
                        "n1": {
                            "categories": [
                                "biolink:" + self.edge.association_output_type
                            ]
                        },
                    },
                    "edges": {
                        "e01": {
                            "subject": "n0",
                            "object": "n1",
                            "predicates": [
                                "biolink:" + self.edge.association_predicate
                            ],
                        }
                    },
                }
            },
            "submitter": "infores:bte",
        }
        return qg

    def construct_request_config(self) -> dict:
        _input = self._get_input()
        config = {
            "url": self._get_url(_input),
            # 'params': json.dumps(self._get_request_body(_input)),
            "data": json.dumps(self._get_request_body(_input)),
            "method": self.query_operation.method,
            "headers": {"Content-Type": "application/json"},
        }
        self.config = config
        return config

    def need_pagination(self, api_response):
        self.has_next = False
        return False

    def get_next(self):
        config = self.construct_request_config()
        return config

    def get_config(self):
        if not self.has_next:
            return self.construct_request_config()
        return self.get_next()
