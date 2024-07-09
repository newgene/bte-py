class EdgeQueryOperation:
    def __init__(self, query_operation: dict):
        self.raw = query_operation

    @property
    def server(self) -> str:
        return self.raw.get("server")

    @property
    def method(self) -> str:
        return self.raw.get("method")

    @property
    def path(self) -> str:
        return self.raw.get("path")

    @property
    def path_params(self) -> dict:
        return self.raw.get("path_params")

    @property
    def params(self) -> dict:
        return self.raw.get("params")

    @property
    def is_query_support_batch(self) -> bool:
        return self.raw.get("support_batch") or False

    @property
    def request_body(self) -> dict:
        return self.raw.get("request_body")

    def get_url(self) -> str:
        return f"{self.server}{self.path}"


class MetaKGEdge:
    def __init__(self, edge):
        self.edge = edge

    @property
    def subject(self) -> str:
        return self.edge["subject"]

    @property
    def predicate(self) -> str:
        return self.edge["predicate"]

    @property
    def object(self) -> str:
        return self.edge["object"]

    @property
    def bte(self) -> dict:
        return self.edge["api"]["bte"]

    @property
    def query_operation(self) -> EdgeQueryOperation:
        return EdgeQueryOperation(self.bte["query_operation"])

    @property
    def response_mapping(self) -> dict:
        return self.bte.get("response_mapping")

    @property
    def input(self) -> str:
        return self.edge.get("input")

    @property
    def association(self) -> dict:
        return self.edge.get("association") or {}

    @property
    def association_input_type(self) -> str:
        return self.association.get("input_type")

    @property
    def association_output_type(self) -> str:
        return self.association.get("output_type")

    @property
    def association_predicate(self) -> str:
        return self.association.get("predicate")
