from typing import List, Dict, Tuple, Any
from .edge import EdgeQueryOperation


class InvalidQuery(Exception):
    def __init__(self, errors, *args):
        self.errors = errors
        super().__init__(errors, *args)


class QueryValidator:
    def __init__(self, metadata: Dict):
        self.metadata = metadata

    @property
    def servers(self) -> List[str]:
        return [server["url"] for server in self.metadata["servers"]]

    @property
    def paths(self) -> Dict:
        return self.metadata["paths"]

    @property
    def components(self) -> Dict:
        return self.metadata["components"]

    def get_field_config_by_ref(self, ref: str) -> Dict:
        fields = ref.replace("#/", "").split("/")

        field_config = self.metadata
        for field in fields:
            field_config = field_config.get(field)
            if not field_config:
                return
        return field_config

    def get_spec_parameters(
        self, path: str, method: str
    ) -> Tuple[List[Dict], List[str]]:
        raw_params = self.paths[path][method].get("parameters") or []
        params = []
        missing_fields = []
        for param in raw_params:
            if "$ref" not in param:
                params.append(param)
                continue

            ref = param["$ref"]
            field_config = self.get_field_config_by_ref(ref)
            if field_config:
                params.append(field_config)
            else:
                missing_fields.append(ref)
        return params, missing_fields

    def validate_query(self, query: EdgeQueryOperation):
        """
        This method accept a query which extracted from a parsed MetaKG edge,
        then do validate it thourgh multiple steps to ensure the query is valid.
        If any step has error, then the method stops, and raise an InvalidQuery Exception.

        sample_query = {
            "params": {
                "fields": "entrezgene,pathway.kegg.name",
                "species": "human",
                "size": 1000
            },
            "request_body": {
                "body": {
                    "q": "{{ queryInputs }}",
                    "scopes": "pathway.kegg.id"
                }
            },
            "path": "/query",
            "method": "post",
            "server": "https://mygene.info/v3",
            "support_batch": true
        }
        """

        self.validate_server(query)
        self.validate_path(query)
        self.validate_method(query)
        self.validate_params(query)
        self.validate_request_body(query)

    def validate_server(self, query: EdgeQueryOperation):
        error = None
        if not query.server:
            error = "Missing server"
        if query.server not in self.servers:
            error = f"Unknown server: {query.server}"

        if error:
            raise InvalidQuery(error)

    def validate_path(self, query: EdgeQueryOperation):
        error = None
        if not query.path:
            error = "Missing path"
        if query.path not in self.paths:
            error = f"Unknown path: {query.path}"

        if error:
            raise InvalidQuery(error)

    def validate_method(self, query: EdgeQueryOperation):
        if query.method not in self.paths[query.path]:
            raise InvalidQuery(f"Invalid method: {query.method} for path: {query.path}")

    def validate_params(self, query: EdgeQueryOperation):
        spec_param_configs, missing_fields = self.get_spec_parameters(
            query.path, query.method
        )

        if missing_fields:
            raise InvalidQuery(
                f"Missing fields: {', '.join(missing_fields)} "
                f"for path: {query.path} with method: {query.method}"
            )

        try:
            self.ensure_fields_in_spec_params(spec_param_configs, query.params)
        except InvalidQuery as ex:
            raise InvalidQuery(
                f"Invalid field for path: {query.path} with method: {query.method}"
            ) from ex

        for spec_param_config in spec_param_configs:
            param_name = spec_param_config["name"]
            _in = spec_param_config["in"]

            try:
                # Check if param appears in right place.
                # NOTE: only support query atm. Will support more places when have samples.
                if _in != "query":
                    raise InvalidQuery(f"Unsupported param: {param_name} in {_in}")

                query_param_value = query.params.get(param_name)
                if not query_param_value:
                    if spec_param_config.get("required"):
                        raise InvalidQuery(f"Missing param: {param_name}")
                    else:
                        continue

                self.validate_schema(spec_param_config["schema"], query_param_value)
            except InvalidQuery as ex:
                raise InvalidQuery(
                    f"Invalid schema for param: {param_name}, path: {query.path}, method: {query.method}"
                ) from ex

    def ensure_fields_in_spec_params(self, spec_param_configs, query_params):
        query_params = query_params or []
        if isinstance(spec_param_configs, list):
            spec_fields = [field_config["name"] for field_config in spec_param_configs]
        else:
            spec_fields = list(spec_param_configs.keys())

        unknown_fields = [field for field in query_params if field not in spec_fields]
        if unknown_fields:
            raise InvalidQuery(f"Unknown fields: {', '.join(unknown_fields)}")

    def validate_schema(self, spec_schema: Dict, value: Any):
        spec_type = spec_schema["type"]

        primitive_types_mapping = {
            "string": str,
            "boolean": bool,
            "integer": (float, int),
        }
        if spec_type in primitive_types_mapping:
            if not isinstance(value, primitive_types_mapping[spec_type]):
                raise InvalidQuery(
                    f"Expect type {spec_type} but "
                    f"receive type {type(value)} instead."
                )
        if spec_type == "object":
            if not isinstance(value, dict):
                raise InvalidQuery(
                    f"Expect type {spec_type} but "
                    f"receive type {type(value)} instead."
                )

            if "properties" not in spec_schema:
                raise InvalidQuery("schem_schema missing properites")

            for field, field_config in spec_schema["properties"].items():
                self.ensure_fields_in_spec_params(field_config, value[field])
                self.validate_schema(field_config, value[field])

        if spec_type == "array":
            if isinstance(value, list):
                _value = value
            else:
                try:
                    _value = value.split(",")
                except Exception:
                    raise InvalidQuery(
                        f"Expect type {spec_type} but "
                        f"receive type {type(value)} instead. value: {value}"
                    )

            for item in _value:
                if spec_schema["items"]["type"] == "object":
                    self.ensure_fields_in_spec_params(spec_schema["items"], item)
                self.validate_schema(spec_schema["items"], item)

    def get_spec_body(self, path: str, method: str) -> Dict:
        try:
            request_body = self.paths[path][method]["requestBody"]
            schema = request_body["content"]["application/json"]["schema"]
            return schema["properties"]
        except Exception as ex:
            raise InvalidQuery("Invalid spec_body") from ex

    def ensure_fields_in_spec_body(self, spec_body_config: Dict, query_body: Dict):
        spec_fields = list(spec_body_config.keys())

        unknown_fields = [field for field in query_body if field not in spec_fields]
        if unknown_fields:
            raise InvalidQuery(f"Unknown fields: {', '.join(unknown_fields)}")

    def validate_request_body(self, query: EdgeQueryOperation):
        spec_body_config = self.get_spec_body(query.path, query.method)

        body = query.request_body["body"]

        self.ensure_fields_in_spec_body(spec_body_config, body)

        for field, field_config in spec_body_config.items():
            try:
                query_value = body.get(field)
                self.validate_schema(field_config, query_value)
            except InvalidQuery as ex:
                raise InvalidQuery(
                    f"Invalid request body for path: {query.path}, method: {query.method}"
                ) from ex
