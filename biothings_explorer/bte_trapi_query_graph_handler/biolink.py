import os
from biothings_explorer.biolink_model.biolink import BioLink


class BioLinkModel:
    def __init__(self):
        biolink_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'biolink.json'))
        self.biolink = BioLink()
        self.biolink.load_sync(biolink_file)

    def reverse(self, predicate):
        if isinstance(predicate, str):
            if predicate in self.biolink.slot_tree.objects:
                if self.biolink.slot_tree.objects[predicate]['symmetric']:
                    return predicate
            return self.biolink.slot_tree.objects[predicate]['inverse']
        return None

    def get_descendant_classes(self, class_name):
        if class_name in self.biolink.class_tree.objects:
            descendants = [entity.name for entity in self.biolink.class_tree.get_descendants(class_name)]
            return [*descendants, class_name]
        return class_name

    def get_descendant_predicates(self, predicate):
        if predicate in self.biolink.slot_tree.objects:
            descendants = [entity.name for entity in self.biolink.slot_tree.get_descendants(predicate)]
            return [*descendants, predicate]
        return [predicate]


BioLinkModelInstance = BioLinkModel()
