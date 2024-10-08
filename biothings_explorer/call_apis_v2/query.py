import json
import logging
from collections.abc import Iterable
from typing import List, Union

from utils.metakg.api import API

from .builder import builder_factory
from .edge import MetaKGEdge
from .helpers import iter_n
from .parser import format_response_v2
from .query_validator import QueryValidator

logger = logging.getLogger(__name__)


class SmartAPI:
    def __init__(self, url, id=None):
        self.url = url
        self._id = id
        self._api = API(url=url, id=id)

    @property
    def metakg(self):
        if not hasattr(self, "_metakg"):
            self._metakg = self._api.get_metakg()
        return self._metakg

    @property
    def query_validator(self):
        return QueryValidator(self._api.smartapi_doc)

    def list_metakg(self) -> List[MetaKGEdge]:
        return [MetaKGEdge(record) for record in self.metakg]

    def _get_edge(
        self,
        metakg_edge: MetaKGEdge,
        input_ids: Union[str, List[str], Iterable[str]],
        validate_edge: bool = True,
        raw: bool = False,
    ):
        query_operation = metakg_edge.query_operation
        if validate_edge:
            self.query_validator.validate_query(query_operation)

        query_builder = builder_factory(metakg_edge, self._api.is_trapi)
        request_func = query_builder.get_request_func()
        request_config = query_builder.construct_request_config(
            {"queryInputs": input_ids}
        )
        logger.info(json.dumps(request_config, indent=2))
        resp = request_func(**request_config)
        resp.raise_for_status()

        resp_data = resp.json()
        if not isinstance(resp_data, list):
            resp_data = [resp_data]
        logger.info("API call is completed.")
        if raw:
            return resp_data
        else:
            # edges = [edge for edge in resp_data if not edge.get("notfound")]
            # return (result for result in format_response(edges, metakg_edge))
            return (result for result in format_response_v2(resp_data, metakg_edge))

    def get_edge(
        self, metakg_edge: MetaKGEdge, input_ids: Union[str, list[str], Iterable[str]], batch_size: int = 1000
    ):
        self.query_validator.validate_query(metakg_edge.query_operation)

        for id_batch in iter_n(input_ids, batch_size):
            if metakg_edge.query_operation.is_query_support_batch:
                for edge in self._get_edge(
                    metakg_edge, id_batch, validate_edge=False
                ):
                    yield edge
            else:
                for input_id in id_batch:
                    for edge in self._get_edge(
                        metakg_edge, input_id, validate_edge=False
                    ):
                        yield edge

    def get_edges(
        self,
        metakg_edges: Union[list[MetaKGEdge], tuple[MetaKGEdge], Iterable[MetaKGEdge]],
        input_ids: Union[str, list[str], Iterable[str]],
        batch_size: int = 1000,
    ):
        for metakg_edge in metakg_edges:
            logger.info("Processing edge: %s", metakg_edge)
            yield from self.get_edge(metakg_edge, input_ids, batch_size=batch_size)