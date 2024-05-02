from typing import List, Dict, Tuple


class InvalidQuery(Exception):
    def __init__(self, errors, *args):
        super().__init__(*args)
        self.errors = errors


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
        fields = ref.replace("#", "").split("/")

        field_config = self.metadata
        for field in fields:
            field_config = getattr(field_config, field, None)

    def get_parameters(self, path: str, method: str) -> Tuple[List[Dict], List[str]]:
        raw_params = self.paths[path][method]
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

    def validate_query(self, query: Dict):
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
        self.validate_support_batch(query)

    def validate_server(self, query):
        server = query.get("server")
        error = None
        if not server:
            error = "Missing server"
        if server not in self.servers:
            error = f"Unknown server: {server}"

        if error:
            raise InvalidQuery(error)

    def validate_path(self, query):
        error = None
        path = query.get("path")
        if not path:
            error = "Missing path"
        if path not in self.paths:
            error = f"Unknown path: {path}"

        if error:
            raise InvalidQuery(error)

    def validate_method(self, query):
        path = query["path"]
        method = query["method"]

        if method not in self.paths[path]:
            raise InvalidQuery(f"Invalid method: {method} for path: {path}")

    def validate_params(self, query):
        path = query["path"]
        method = query["method"]
        query_params = query["params"]

        spec_param_configs, missing_fields = self.get_parameters(path, method)

        if missing_fields:
            raise InvalidQuery(
                f"Missing fields: {', '.join(missing_fields)} "
                f"for path: {path} with method: {method}"
            )

        errors = {}
        for spec_param_config in spec_param_configs:
            param_name = spec_param_config["name"]
            _in = spec_param_config["in"]

            # Check if param appears in right place.
            # NOTE: only support query atm. Will support more places when have samples.
            if _in != "query":
                raise InvalidQuery(
                    f"Unsupported param: {param_name} in {_in} "
                    f"for path: {path} with method: {method}"
                )

            query_param_value = query_params.get(param_name)
            if spec_param_config.get("required") and not query_param_value:
                errors[param_name] = f"Missing param: {param_name}"

            try:
                self.validate_param_schema(
                    spec_param_config["schema"], query_param_value
                )
            except InvalidQuery as ex:
                raise InvalidQuery(
                    f"Invalid schema for param: {param_name}, path: {path}, method: {method}"
                ) from ex

    def validate_param_schema(self, spec_schema, value):
        spec_type = spec_schema["type"]

        primitive_types_mapping = {
            "string": str,
            "boolean": bool,
            "integer": float,
        }
        if spec_type in primitive_types_mapping:
            if not isinstance(value, primitive_types_mapping[spec_type]):
                raise InvalidQuery(
                    f"Expect type {spec_type} but "
                    f"receive type {type(value)} instead."
                )
        if spec_type == "object":
            pass
        if spec_type == "array":
            pass

    def validate_request_body(self, query):
        """
        "request_body": {
            "body": {
                "q": "{{ queryInputs }}",
                "scopes": "pathway.kegg.id"
            }
        }
        """

    def validate_support_batch(self, query):
        """
        "support_batch": true
        """
