class KGNode:
    def __init__(self, _id, info):
        self.id = _id
        self._primary_id = info['primary_id']
        self._qg_id = info['qg_id']
        self._curies = info['equivalent_ids']
        self._names = info['names']
        self._semantic_type = info['category']
        self._node_attributes = info['node_attributes']
        self._label = info['label']
        self._source_nodes = set()
        self._target_nodes = set()
        self._source_qg_nodes = set()
        self._target_qg_nodes = set()

    def add_source_node(self, kg_node):
        self._source_nodes.add(kg_node)

    def add_target_node(self, kg_node):
        self._target_nodes.add(kg_node)

    def add_source_qg_node(self, qg_node):
        self._source_qg_nodes.add(qg_node)

    def add_target_qg_node(self, qg_node):
        self._target_qg_nodes.add(qg_node)
