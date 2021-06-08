class TRAPIQueryBuilder:
    def __init__(self, edge):
        self.start = 0
        self.has_next = False
        self.edge = edge

    def get_url(self):
        return self.edge['query_operation']['server'] + self.edge['query_operation']['path']

    def _get_url(self, edge, _input):
        server = edge['query_operation']['server']
        if server.endswith('/'):
            server = server[:len(server) - 1]
        path = edge['query_operation']['path']
        if isinstance(edge['query_operation']['path_params'], list):
            for param in edge['query_operation']['path_params']:
                val = edge['query_operation']['params'][param]
                path = path.replace('{' + param + '}', val).replace('{inputs[0]}', _input)
        return server + path

    def _get_input(self, edge):
        return edge['input']

    def _get_request_body(self, edge, _input):
        qg = {
            "message": {
                "query_graph": {
                    "nodes": {
                        "n0": {
                            "ids": _input if isinstance(_input, list) else [_input],
                            "categories": ["biolink:" + edge['association']['input_type']]
                        },
                        "n1": {
                            "categories": ["biolink:" + edge['association']['output_type']]
                        }
                    },
                    "edges": {
                        "e01": {
                            "subject": "n0",
                            "object": "n1",
                            "predicates": ["biolink:" + edge['association']['predicate']]
                        }
                    }
                }
            }
        }
        return qg

    def construct_request_config(self):
        _input = self._get_input(self.edge)
        config = {
            'url': self._get_url(self.edge, _input),
            'params': self._get_request_body(self.edge, _input),
            'method': self.edge['query_operation']['method'],
            'headers': {
                'Content-Type': 'application/json'
            }
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
