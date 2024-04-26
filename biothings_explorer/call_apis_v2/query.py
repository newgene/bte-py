import logging

import requests

from .helpers import yaml_2_json
from .metakg.parser import MetaKGParser


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

        return resp_data

    def get_edges(self, metakg_edge, input_ids):
        """<batch of the get_edge>"""

    def format_response(self, metakg_edge, resp_data):
        output = []
        subject_type = metakg_edge["subject"]
        object_type = metakg_edge["object"]
        predicate = metakg_edge["predicate"]
        response_mapping = metakg_edge["bte"]["response_mapping"][predicate]

        # Determine object fields using mapping and prepare to extract values
        object_fields = {
            key: value.split(".") for key, value in response_mapping.items()
        }

        for item in resp_data:
            # Dynamically determine the subject ID
            subject_id = self.determine_subject_id(item, ["_id", "entrezgene", "query"])
            if not subject_id:
                logger.warning("Cannot found subject_id")
                return []

            for field_name, path in object_fields.items():
                current_data = item
                # Navigate through nested structures
                for part in path:
                    if isinstance(current_data, dict) and part in current_data:
                        current_data = current_data[part]
                    elif isinstance(current_data, list):
                        current_data = [
                            obj.get(part) for obj in current_data if part in obj
                        ]
                    else:
                        current_data = None
                        break

                # Process multiple objects or single object scenarios
                if isinstance(current_data, list):
                    for obj in current_data:
                        formatted_item = self.create_formatted_item(
                            subject_type,
                            subject_id,
                            object_type,
                            predicate,
                            field_name,
                            obj,
                        )
                        output.append(formatted_item)
                elif current_data:
                    formatted_item = self.create_formatted_item(
                        subject_type,
                        subject_id,
                        object_type,
                        predicate,
                        field_name,
                        current_data,
                    )
                    output.append(formatted_item)

        return output

    def determine_subject_id(self, item, possible_keys):
        """Attempts to determine the subject ID from a list of possible keys"""

        if isinstance(item, str):
            for key in possible_keys:
                if key == item:
                    return key
        else:
            for key in possible_keys:
                if key in item:
                    return item[key]
            # If no key directly found, guess based on the first key that looks like an identifier
            for key in item.keys():
                if "id" in key or "ID" in key:
                    return item[key]
            return  # If nothing suitable is found, return None

    def create_formatted_item(
        self,
        subject_type,
        subject_field,
        subject_id,
        object_type,
        predicate,
        field_name,
        object_id,
    ):
        """Helper function to create a formatted dictionary item"""
        return {
            "subject": {"type": subject_type, subject_field: subject_id},
            "predicate": predicate,
            "object": {"type": object_type, field_name: object_id},
        }
