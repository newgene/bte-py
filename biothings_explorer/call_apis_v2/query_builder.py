import functools
import json

import httpx
from jinja2 import Environment


class QueryBuilder:
    def __init__(self, edge):
        self.edge = edge

    def get_url(self):
        return (
            self.edge["query_operation"]["server"]
            + self.edge["query_operation"]["path"]
        )

    def _get_url(self, edge, _input):
        server = edge["query_operation"]["server"]
        if server.endswith("/"):
            server = server[:-1]

        path = edge["query_operation"]["path"]
        if isinstance(edge["query_operation"].get("path_params"), list):
            for param in edge["query_operation"]["path_params"]:
                val = edge["query_operation"]["params"][param]
                # convert list values to single values
                for key, value in enumerate(_input):
                    if isinstance(_input, dict) and isinstance(_input[value], list):
                        _input[value] = _input[value][0]
                if isinstance(_input, dict):
                    path = (
                        Environment()
                        .from_string(path.replace("{" + param + "}", val), _input)
                        .render()
                    )
                else:
                    path = (
                        Environment()
                        .from_string(path.replace("{" + param + "}", val))
                        .render()
                    )

        return server + path

    def _get_input(self, edge):
        return edge["input"]

    def _get_params(self, edge, _input):
        params = {}
        for param in edge["query_operation"]["params"]:
            if (
                isinstance(edge["query_operation"].get("path_params"), list)
                and param in edge["query_operation"]["path_params"]
            ):
                continue
            if isinstance(edge["query_operation"]["params"].get(param), str):
                if isinstance(_input, dict):
                    params[param] = (
                        Environment()
                        .from_string(edge["query_operation"]["params"][param], _input)
                        .render()
                    )
                else:
                    params[param] = (
                        Environment()
                        .from_string(edge["query_operation"]["params"][param])
                        .render()
                    )
            else:
                params[param] = edge["query_operation"]["params"][param]
        return params

    def _get_request_body(self, edge, _input):
        if (
            edge["query_operation"].get("request_body")
            and "body" in edge["query_operation"]["request_body"]
        ):
            body = edge["query_operation"]["request_body"]["body"]

            if isinstance(body, dict):
                data_template = Environment().from_string(body, _input).render()
                data = json.loads(data_template)
            else:
                try:
                    reduced = functools.reduce(
                        lambda prev, current: prev
                        + current
                        + "="
                        + Environment().from_string(str(body[current]), _input).render()
                        + "&",
                        body,
                        "",
                    )
                except ValueError:
                    reduced = functools.reduce(
                        lambda prev, current: prev
                        + current
                        + "="
                        + Environment().from_string(str(body[current])).render()
                        + "&",
                        body,
                        "",
                    )
                data = reduced[:-1]

            return data

    def construct_request_config(self):
        _input = self._get_input(self.edge)
        return {
            "url": self._get_url(self.edge, _input),
            "params": self._get_params(self.edge, _input),
            "data": self._get_request_body(self.edge, _input),
            "headers": {"Content-Type": "application/json"},
        }

    def get_request_func(self):
        return getattr(httpx, self.edge.query_operation["method"])
