import requests

from .helpers import yaml_2_json
from .metakg.parser import MetaKGParser


class SmartAPI:
    def __init__(self, url):
        self.url = url

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
            self.metakg_errors = None  # reset metakg_errors
            if self.is_trapi:
                self._metakg = mkg_parser.get_TRAPI_metadatas(self.metadata)
            else:
                self._metakg = mkg_parser.get_non_TRAPI_metadatas(self.metadata)
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
            }
            for record in self.metakg
        ]

    def get_edge(self, one_metakg_edge, input_id):
        """<call API with the input_id, based on one_metakg_edge, process response, then return response edge(s)>"""

    def get_edges(self, one_metakg_edge, a_list_of_input_ids):
        """<batch of the get_edge>"""
