import json

import httpx

from .jinja import jinja_env


class TemplateQueryBuilder:
    def __init__(self, edge):
        self.edge = edge

    @property
    def query_operation(self):
        return self.edge["bte"]["query_operation"]

    def get_url(self):
        return self.query_operation["server"] + self.query_operation["path"]

    def _get_url(self, _input):
        server = self.query_operation["server"]
        if server.endswith("/"):
            server = server[:-1]

        path = self.query_operation["path"]
        if isinstance(self.query_operation.get("path_params"), list):
            for param in self.query_operation["path_params"]:
                val = self.query_operation["params"][param]
                # convert list values to single values
                for key, value in enumerate(_input):
                    if isinstance(_input, dict) and isinstance(_input[value], list):
                        _input[value] = _input[value][0]
                if isinstance(_input, dict):
                    path = jinja_env.from_string(
                        path.replace("{" + param + "}", val), _input
                    ).render()
                else:
                    path = jinja_env.from_string(
                        path.replace("{" + param + "}", val)
                    ).render()

        return server + path

    def _get_params(self, _input):
        params = {}
        for param in self.query_operation["params"]:
            if (
                isinstance(self.query_operation.get("path_params"), list)
                and param in self.query_operation["path_params"]
            ):
                continue
            if isinstance(self.query_operation["params"].get(param), str):
                if isinstance(_input, dict):
                    params[param] = jinja_env.from_string(
                        self.query_operation["params"][param], _input
                    ).render()
                else:
                    params[param] = jinja_env.from_string(
                        self.query_operation["params"][param]
                    ).render()
            else:
                params[param] = self.query_operation["params"][param]
        return params

    def _get_request_body(self, _input):
        if (
            self.query_operation.get("request_body")
            and "body" in self.query_operation["request_body"]
        ):
            body = self.query_operation["request_body"]["body"]

            if isinstance(body, str):
                data_template = jinja_env.from_string(body, _input).render()
                data = json.loads(data_template)
            elif isinstance(body, dict):
                data = {}
                for field, value in body.items():
                    try:
                        data[field] = jinja_env.from_string(str(value), _input).render()
                    except ValueError:
                        data[field] = jinja_env.from_string(str(value)).render()
            else:
                raise Exception("body is invalid format")

            return data

    def construct_request_config(self, _input):
        return {
            "url": self._get_url(_input),
            "params": self._get_params(_input),
            "json": self._get_request_body(_input),
            "headers": {"Content-Type": "application/json"},
        }

    def get_request_func(self):
        return getattr(httpx, self.query_operation["method"])
