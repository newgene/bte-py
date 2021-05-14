from os.path import abspath


class MetaKG:
    _ops = []
    path = ''
    predicates_path = ''

    def __init__(self, path, predicates_path):
        self._ops = []
        self.path = path
        self.predicates_path = predicates_path

    @property
    def path(self):
        return self.path

    @path.setter
    def path(self, file_path):
        if not file_path:
            self._file_path = abspath(file_path)
        else:
            self._file_path = file_path

    @property
    def ops(self, value):
        return self._ops
