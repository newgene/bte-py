from jinja2 import Environment, BaseLoader
import functools
import json


class TemplateQueryBuilder:
    def __init__(self, edge):
        self.start = 0
        self.has_next = False
        self.edge = edge

    def get_url(self):
        return self.edge['query_operation']['server'] + self.edge['query_operation']['path']

    def _get_url(self, edge, _input):
        server = edge['query_operation']['server']
        if server.endswith('/'):
            server = server[0:len(server) - 1]
        path = edge['query_operation']['path']
        if isinstance(edge['query_operation'].get('path_params'), list):
            for param in edge['query_operation']['path_params']:
                val = edge['query_operation']['params'][param]
                if isinstance(_input, dict):
                    path = Environment().from_string(path.replace("{" + param + "}", val), _input).render()
                else:
                    path = Environment().from_string(path.replace("{" + param + "}", val)).render()

        return server + path

    def _get_input(self, edge):
        return edge['input']

    def _get_params(self, edge, _input):
        params = {}
        for param in edge['query_operation']['params']:
            if isinstance(edge['query_operation'].get('path_params'), list) and param in edge['query_operation']['path_params']:
                return
            if isinstance(edge['query_operation']['params'].get(param), str):
                if isinstance(_input, dict):
                    params[param] = Environment().from_string(edge['query_operation']['params'][param], _input).render()
                else:
                    params[param] = Environment().from_string(edge['query_operation']['params'][param]).render()
            else:
                params[param] = edge['query_operation']['params'][param]
        return params

    def _get_request_body(self, edge, _input):
        if edge['query_operation'].get('request_body') and 'body' in edge['query_operation']['request_body']:
            body = edge['query_operation']['request_body']['body']
            if isinstance(edge['query_operation'].get('requestBodyType'), dict):
                if isinstance(_input, dict):
                    data_template = Environment().from_string(body, _input).render()
                else:
                    data_template = Environment().from_string(body, _input).render()

                data = json.loads(data_template)
            else:
                reduced = functools.reduce(lambda prev, current: prev + current + "=" +
                                           (Environment().from_string(str(body[current]), _input).render()
                                            if isinstance(str(body[current]), dict) else
                                            Environment().from_string(str(body[current])).render()) + "&",
                                           body, "")
                data = reduced[0:len(reduced) - 1]
            return data

    def construct_axios_request_config(self):
        _input = self._get_input(self.edge)
        config = {
            'url': self._get_url(self.edge, _input),
            'params': self._get_params(self.edge, _input),
            'data': self._get_request_body(self.edge, _input),
            'method': self.edge['query_operation'].get('method'),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
        self.config = config
        return config

    def need_pagination(self, api_response):
        if self.edge['query_operation']['method'] == 'get' and 'biothings' in self.edge['tags']:
            if api_response['total'] > self.start + len(api_response['hits']):
                if self.start + len(api_response['hits']) < 10000:
                    self.has_next = True
                    return True
        self.has_next = False
        return False

    def get_next(self):
        self.start = min(self.start + 1000, 9999)
        config = self.construct_axios_request_config()
        config['params']['from'] = self.start
        if config['params']['size'] + self.start > 10000:
            config['params']['size'] = 10000 - self.start
        self.config = config
        return config

    def get_config(self):
        if not self.has_next:
            return self.construct_axios_request_config()
        return self.get_next()
