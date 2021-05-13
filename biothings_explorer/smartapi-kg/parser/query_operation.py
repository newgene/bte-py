class QueryOperationObject:
    _params = {}
    _request_body = {}
    _support_batch = None
    _input_separator = ''
    _path = ''
    _method = ''
    _server = ''
    _tags = []
    _path_params = []

    @property.setter
    def xBTEKGSOperation(self, new_op):
        self._params = new_op.parameters
        self._request_body = new_op.request_body
        self._support_batch = new_op.support_batch
        self._input_separator = new_op.input_separator

    @property
    def params(self):
        return self._params

    @property
    def request_body(self):
        return self._request_body

    @property
    def input_separator(self):
        return self._input_separator

    @property.setter
    def path(self, new_path):
        self._path = new_path

    @property
    def path(self):
        return self._path

    @property
    def method(self):
        return self._method

    @property.setter
    def method(self, new_method):
        self._method = new_method

    @property
    def server(self):
        return self._server

    @property.setter
    def server(self, new_server):
        self._server = new_server

    @property
    def tags(self):
        return self._tags

    @property.setter
    def tags(self, new_tags):
        self._tags = new_tags

    @property
    def path_params(self):
        return self._path_params

    @property
    def path_params(self, new_path_params):
        self._path_params = new_path_params
