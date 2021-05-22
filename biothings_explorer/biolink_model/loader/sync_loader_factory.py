import os
from .sync_default_loader import SyncDefaultLoader
from .sync_file_loader import SyncFileLoader


def sync_loader(source=None):
    if not source:
        return SyncDefaultLoader()
    if os.path.isfile(source):
        return SyncFileLoader()
    raise Exception('Your input is invalid. It should be undefined or a valid url or a valid file path.')
