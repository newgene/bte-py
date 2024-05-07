import json
import logging

import httpx

from .helpers import yaml_2_json
from .metakg.parser import MetaKGParser
from .parser import format_response
from .query_validator import QueryValidator


logger = logging.getLogger(__name__)


class SmartAPI:
    def __init__(self, url, id=None):
        self.url = url
        self._id = id

    @property
    def metadata(self):
        if not hasattr(self, "_metadata"):
            resp = httpx.get(self.url)
            resp.raise_for_status()

            try:
                self._metadata = yaml_2_json(resp.text)
            except Exception:
                try:
                    self._metadata = json.loads(resp.text)
                except Exception:
                    raise Exception("Cannot parse the metadata from the URL")

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

    @property
    def query_validator(self):
        return QueryValidator(self.metadata)

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

    def get_edge(self, metakg_edge, input_id, validate_edge=True):
        query_operation = metakg_edge["bte"]["query_operation"]
        if validate_edge:
            self.query_validator.validate_query(query_operation)

        request_method = getattr(httpx, query_operation["method"])
        url = query_operation["server"] + query_operation["path"]
        params = query_operation["params"]
        body = query_operation["request_body"]["body"]
        body["q"] = input_id

        resp = request_method(url, params=params, data=body)
        resp.raise_for_status()

        resp_data = resp.json()
        if not isinstance(resp_data, list):
            resp_data = [resp_data]

        edges = [edge for edge in resp_data if not edge.get("notfound")]
        return (result for result in format_response(edges, metakg_edge))

    def get_edges(self, metakg_edge, input_ids, batch_size=1000):
        query_operation = metakg_edge["bte"]["query_operation"]
        self.query_validator.validate_query(query_operation)

        results = []
        for i in range(0, len(input_ids), batch_size):
            start_index = i
            end_index = i + batch_size
            sub_input_ids = input_ids[start_index:end_index]

            if query_operation["support_batch"]:
                combined_ids = ",".join(sub_input_ids)
                results.append(
                    self.get_edge(metakg_edge, combined_ids, validate_edge=False)
                )
            else:
                results += [
                    self.get_edge(metakg_edge, input_id, validate_edge=False)
                    for input_id in sub_input_ids
                ]

        return results
