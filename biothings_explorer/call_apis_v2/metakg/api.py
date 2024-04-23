from .component import Components
from .endpoint import Endpoint


class API:
    _smartapi_doc = {}

    def __init__(self, smartapi_doc):
        self._smartapi_doc = smartapi_doc

    @classmethod
    def get_default_server_url(cls, servers):
        """Get the default server from the servers list."""
        # return the first server with production maturity
        for server in servers:
            if server.get("x-maturity", None) == "production":
                return server.get("url")
        # then check for description for word "production"
        for server in servers:
            if server.get("description", "").lower().find("production") != -1:
                return server.get("url")
        # then use https URL first
        for server in servers:
            if server.get("url", "").startswith("https"):
                return server.get("url")
        # finally, just return the first available one
        return servers[0].get("url")

    @property
    def smartapi_doc(self):
        return self._smartapi_doc

    @property
    def metadata(self):
        metadata = self.fetch_API_meta()
        metadata["operations"] = self.fetch_all_opts()
        return metadata

    def fetch_API_title(self):
        if "info" not in self.smartapi_doc:
            return None
        return self.smartapi_doc["info"]["title"]

    def fetch_XTranslator_component(self):
        if "info" not in self.smartapi_doc:
            return None
        if "x-translator" not in self.smartapi_doc["info"]:
            return None
        return self.smartapi_doc["info"]["x-translator"]["component"]

    def fetch_XTranslator_team(self):
        if "info" not in self.smartapi_doc:
            return []
        if "x-translator" not in self.smartapi_doc["info"]:
            return []
        return self.smartapi_doc["info"]["x-translator"]["team"]

    def fetch_API_tags(self):
        if "tags" not in self.smartapi_doc:
            return None
        return [x["name"] for x in self.smartapi_doc["tags"]]

    def fetch_server_url(self):
        if "servers" not in self.smartapi_doc:
            return None
        return self.get_default_server_url(self.smartapi_doc["servers"])

    def fetch_components(self):
        if "components" not in self.smartapi_doc:
            return None
        return Components(self.smartapi_doc["components"])

    def fetch_API_meta(self):
        return {
            "title": self.fetch_API_title(),
            "tags": self.fetch_API_tags(),
            "url": self.fetch_server_url(),
            "x-translator": {
                "component": self.fetch_XTranslator_component(),
                "team": self.fetch_XTranslator_team(),
            },
            "smartapi": {
                "id": self.smartapi_doc.get("_id"),
                "meta": self.smartapi_doc.get("_meta"),
            },
            "components": self.fetch_components(),
            "paths": (
                list(self.smartapi_doc["paths"].keys())
                if isinstance(self.smartapi_doc.get("paths"), dict)
                else []
            ),
            "operations": [],
        }

    def fetch_all_opts(self):
        ops = []
        api_meta = self.fetch_API_meta()
        if "paths" in self.smartapi_doc:
            for path in self.smartapi_doc["paths"].keys():
                ep = Endpoint(self.smartapi_doc["paths"][path], api_meta, path)
                ops = [*ops, *ep.construct_endpoint_info()]
        return ops
