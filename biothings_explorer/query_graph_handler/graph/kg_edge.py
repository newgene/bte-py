class KGEdge:
    def __init__(self, _id, info):
        self.id = _id
        self.predicate = info['predicate']
        self.subject = info['subject']
        self.object = info['object']
        self.apis = set()
        self.infores_curies = set()
        self.sources = set()
        self.publications = set()
        self.attributes = {}

    def add_api(self, api):
        if not api:
            return
        if not isinstance(api, list):
            api = [api]

        for item in api:
            self.apis.add(item)

    def add_source(self, source):
        if not source:
            return
        if not isinstance(source, list):
            source = [source]
        for item in source:
            self.sources.add(item)

    def add_infores_curie(self, infores_curie):
        if not infores_curie:
            return
        if not isinstance(infores_curie, list):
            infores_curie = [infores_curie]
        for item in infores_curie:
            self.infores_curies.add(item)

    def add_publication(self, publication):
        if not publication:
            return
        if not isinstance(publication, list):
            publication = [publication]
        for item in publication:
            self.publications.add(item)

    def add_additional_attributes(self, name, value):
        self.attributes[name] = value
