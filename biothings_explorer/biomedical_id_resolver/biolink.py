from biothings_explorer.biolink_model.index import BioLink


class BioLinkHandler:
    instance = {}
    _class_tree = BioLink.class_tree

    def __init__(self):
        if not BioLinkHandler.instance:
            biolink = BioLink()
            biolink.load_sync()
            self._class_tree = biolink.class_tree

    @property
    def class_tree(self):
        return self._class_tree


BioLinkHandlerInstance = BioLinkHandler()