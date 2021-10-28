import functools
from .template_funcs import rm_prefix, repl_prefix, slice


class QueryBuilder:
    def __init__(self, edge):
        self.start = 0
        self.has_next = False
        self.edge = edge

    def get_url(self):
        return self.edge['query_operation']['server'] + self.edge['query_operation']['path']

    def _get_url(self, edge, raw_input):
        server = edge['query_operation']['server']
        if server.endswith('/'):
            server = server[0: len(server) - 1]
        path = edge['query_operation']['path']
        if isinstance(edge['query_operation'].get('path_params'), list):
            for param in edge['query_operation']['path_params']:
                val = edge['query_operation']['params'][param]
                _input = raw_input
                if isinstance(raw_input, list):
                    _input = str(raw_input)[1:-1]

                path = path.replace('{' + param + "}", val).replace("{inputs[0]}", _input)
        return server + path

    def _get_input(self, edge):
        if edge['query_operation'].get('supportBatch'):
            if isinstance(edge['input'], list):
                return edge['query_operation'].get("inputSeparator", ',').join(edge['input'])
        return edge['input']

    def _get_params(self, edge, raw_input):
        params = {}
        for param in edge['query_operation']['params']:
            if isinstance(edge['query_operation'].get('path_params'), list) and param in edge['query_operation']['path_params']:
                continue
            if isinstance(edge['query_operation']['params'][param], str):
                _input = raw_input
                if isinstance(raw_input, list):
                    _input = str(raw_input)[1:-1]

                params[param] = edge['query_operation']['params'][param].replace("{inputs[0]}", _input)
            else:
                params[param] = edge['query_operation']['params'][param]
        return params

    def _get_request_body(self, edge, raw_input):
        if edge['query_operation'].get('request_body') and 'body' in edge['query_operation'].get('request_body'):
            for key in edge['query_operation']['request_body']['body']:
                try:
                    _input = raw_input
                    if isinstance(raw_input, list):
                        _input = str(raw_input)[1:-1]
                    edge['query_operation']['request_body']['body'][key] = edge['query_operation']['request_body']['body'][key].replace('{inputs[0]}', _input)
                except AttributeError:
                    pass

            return edge['query_operation']['request_body']['body']

    # axios has a different config from python requests so params and data are swapped
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
        if not config.get('params'):
            config['params'] = {}
        config['params']['from'] = self.start
        self.config = config
        return config

    def get_config(self):
        if not self.has_next:
            return self.construct_request_config()
        return self.get_next()
