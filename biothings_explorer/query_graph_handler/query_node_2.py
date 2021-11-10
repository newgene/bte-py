class QNode:
    def __init__(self, _id, info):
        self.id = _id
        self.category = info['categories'] or 'NamedThing'
        self.entity = info['ids']
        self.entity_count = len(info['ids']) if info['ids'] else 0
        self.results = []

    def update_curies(self, curies):
        if not self.curie:
            self.curie = []
        if len(self.curie):
            self.curie = list(set(self.curie) & set(curies))
        else:
            self.curie = curies
        self.entity_count = len(self.curie)