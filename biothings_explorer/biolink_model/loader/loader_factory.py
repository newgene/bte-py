import os
from .default_loader import DefaultLoader
from .file_loader import FileLoader
from .url_loader import URLLoader


def loader(source=None):
    if not source:
        return DefaultLoader()
    if source.startswith('http://') or source.startswith('https://'):
        return URLLoader()
    if os.path.isfile(source):
        return FileLoader()
    else:
        raise Exception('Your input is invalid. It should be undefined or a valid url or a valid file path.')
