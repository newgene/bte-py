from biothings_explorer.biomedical_id_resolver.resolve.biolink_based_resolver import BioLinkBasedResolver
from biothings_explorer.biomedical_id_resolver.resolve.default_resolver import DefaultResolver
from .config import APIMETA
from .fake import generate_invalid


class Resolver:
    _resolver = {}

    def __init__(self, _type):
        self.set_resolver(_type)

    def set_resolver(self, _type):
        if _type == 'biolink':
            self._resolver = BioLinkBasedResolver()
        else:
            self._resolver = DefaultResolver()

    @property
    def resolver(self):
        return self._resolver

    @resolver.setter
    def resolver(self, _type):
        self.set_resolver(_type)


METADATA = APIMETA


def generate_invalid_bioentities(_input):
    return generate_invalid(_input)
