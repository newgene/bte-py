from .transformers.biolink_transformer import BiolinkTransformer
from .transformers.biothings_transformer import BioThingsTransformer
from .transformers.cord_transformer import CordTransformer
from .transformers.ctd_transformer import CTDTransformer
from .transformers.semmed_transformer import SemmedTransformer
from .transformers.opentarget_transformer import OpenTargetTransformer
from .transformers.transformer import BaseTransformer
from .transformers.trapi_transformer import TRAPITransformer


class Transformer:
    data = {}
    tg = {}

    def __init__(self, data):
        self.data = data
        self.route()

    def route(self):
        api = self.data['edge']['association']['api_name']
        tags = self.data['edge']['query_operation']['tags']
        if 'bte-trapi' in tags:
            self.tf = TRAPITransformer(self.data)
        elif api.startswith('CORD'):
            self.tf = CordTransformer(self.data)
        elif api.startswith('SEMMED'):
            self.tf = SemmedTransformer(self.data)
        elif api.startswith('BioLink API'):
            self.tf = BiolinkTransformer(self.data)
        elif api.startswith('biothings'):
            self.tf = BioThingsTransformer(self.data)
        elif api.startswith('ctd'):
            self.tf = CTDTransformer(self.data)
        elif api.startswith('opentarget'):
            self.tf = OpenTargetTransformer(self.data)
        else:
            self.tf = BaseTransformer(self.data)

    def transform(self):
        return self.tf.transform()
