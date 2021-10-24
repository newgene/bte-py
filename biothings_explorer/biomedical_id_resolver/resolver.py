from biothings_explorer.biomedical_id_resolver.resolve.biolink_based_resolver import BioLinkBasedResolver
from biothings_explorer.biomedical_id_resolver.resolve.default_resolver import DefaultResolver
from .config import APIMETA
from .fake import generate_invalid
from .sri import query, transform_results


class Resolver:
    _resolver = {}

    def __init__(self, _type=None):
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

    def resolve(self, user_input):
        return self._resolver.resolve(user_input)


def resolve_sri(user_input):
    api_input = None
    try:
        if isinstance(user_input, list):
            api_input = user_input
        else:
            api_input = [value for value in user_input.values()]

            # flatten api_input
            api_input = [item for sublist in api_input for item in sublist]
    except Exception as e:
        print("Input is not in the right shape. Expected an array of curies or an object of arrays of curies.")
        return {}
    query_results = query(api_input)
    return transform_results(query_results)


METADATA = APIMETA


def generate_invalid_bioentities(_input):
    return generate_invalid(_input)
