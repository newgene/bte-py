import logging

import requests

from .helpers import yaml_2_json
from .metakg.parser import MetaKGParser
from .parser import format_response


logger = logging.getLogger(__name__)


class SmartAPI:
    def __init__(self, url, id=None):
        self.url = url
        self._id = id

    @property
    def metadata(self):
        if not hasattr(self, "_metadata"):
            resp = requests.get(self.url)
            resp.raise_for_status()
            self._metadata = yaml_2_json(resp.text)
        return self._metadata

    @property
    def metakg(self):
        if not hasattr(self, "_metakg"):
            mkg_parser = MetaKGParser()
            extra_data = {"id": self._id, "url": self.url}
            self.metakg_errors = None  # reset metakg_errors
            if self.is_trapi:
                self._metakg = mkg_parser.get_TRAPI_metadatas(self.metadata, extra_data)
            else:
                self._metakg = mkg_parser.get_non_TRAPI_metadatas(
                    self.metadata, extra_data
                )
            if mkg_parser.metakg_errors:
                # hold metakg_errors for later use
                self.metakg_errors = mkg_parser.metakg_errors

        return self._metakg

    def has_tags(self, *tags):
        """return True if an SmartAPI contains all given tags"""
        _tag_set = set([_tag.get("name") for _tag in self.metadata["tags"]])
        return len(set(tags) - _tag_set) == 0

    @property
    def is_trapi(self):
        """return True if a TRAPI"""
        return self.has_tags("trapi", "translator")

    def list_metakg(self):
        return [
            {
                "subject": record["subject"],
                "predicate": record["predicate"],
                "object": record["object"],
                "bte": record["bte"],
            }
            for record in self.metakg
        ]

    def get_edge(self, metakg_edge, input_id):
        query_operation = metakg_edge["bte"]["query_operation"]

        request_method = getattr(requests, query_operation["method"])
        url = query_operation["server"] + query_operation["path"]
        params = query_operation["params"]
        body = query_operation["request_body"]["body"]
        body["q"] = input_id

        resp = request_method(url, params=params, data=body)
        resp.raise_for_status()

        resp_data = resp.json()
        if isinstance(resp_data, list):
            resp_data = resp_data[0]

        if resp_data.get("notfound"):
            return

        return format_response(resp_data, metakg_edge)

    def get_edges(self, metakg_edge, input_ids):
        query_operation = metakg_edge["bte"]["query_operation"]
        if query_operation["support_batch"]:
            combined_ids = ",".join(input_ids)
            return self.get_edge(metakg_edge, combined_ids)

        results = []
        for input_id in input_ids:
            results += self.get_edge(metakg_edge, input_id)
        return results
