import functools


class QueryBuilder:
    def __init__(self, edge):
        self.start = 0
        self.has_next = False
        self.edge = edge

    def get_url(self):
        return self.edge['query_operation']['server'] + self.edge['query_operation']['path']

    def _get_url(self, edge, _input):
        server = edge['query_operation']['server']
        if server.endswith('/'):
            server = server[0: len(server) - 1]
        path = edge['query_operation']['path']
        if isinstance(edge['query_operation'].get('path_params'), list):
            for param in edge['query_operation']['path_params']:
                val = edge['query_operation']['params'][param]
                path = path.replace('{' + param + "}", val).replace("{inputs[0]}", _input)
        return server + path

    def _get_input(self, edge):
        if edge['query_operation']['supportBatch']:
            if isinstance(edge['input'], list):
                return edge['query_operation'].get("inputSeparator", ',').join(edge['input'])
        return edge['input']

    def _get_params(self, edge, _input):
        params = {}
        for param in edge['query_operation']['params']:
            if isinstance(edge['query_operation'].get('path_params'), list) and param in edge['query_operation']['path_params']:
                continue
            if isinstance(edge['query_operation']['params'][param], str):
                params[param] = edge['query_operation']['params'][param].replace("{inputs[0]}", _input)
            else:
                params[param] = edge['query_operation']['params'][param]
        return params

    # TODO CONVERT THIS TO DICT
    def _get_request_body(self, edge, _input):
        if edge['query_operation'].get('request_body') and 'body' in edge['query_operation'].get('request_body'):
            for key in edge['query_operation']['request_body']['body']:
                try:
                    edge['query_operation']['request_body']['body'][key] = edge['query_operation']['request_body']['body'][key].replace('{inputs[0]}', _input)
                except AttributeError:
                    pass

            #body = edge['query_operation']['request_body']['body']
            #reduced = functools.reduce(lambda accumulator, key: accumulator + key + '=' + str(body[key]).replace('{inputs[0]}', _input) + '&', body.keys(), '')
            #return reduced[:len(reduced) - 1]
            return edge['query_operation']['request_body']['body']

    def construct_request_config(self):
        _input = self._get_input(self.edge)
        config = {
            'url': self._get_url(self.edge, _input),
            'params': self._get_request_body(self.edge, _input),
            'data': self._get_params(self.edge, _input),
            'method': self.edge['query_operation']['method']
        }
        return config

    def need_pagination(self, api_response):
        if self.edge['query_operation']['method'] == 'get' and 'biothings' in self.edge['tags']:
            if api_response['total'] > self.start + len(api_response['hits']):
                self.has_next = True
                return True
        self.has_next = False
        return False

    def get_next(self):
        self.start += 1000
        config = self.construct_request_config()
        config['params']['from'] = self.start
        self.config = config
        return config

    def get_config(self):
        if not self.has_next:
            return self.construct_request_config()
        return self.get_next()
