class SizeHandler:
    def __init__(self,builder):
        self._builder = builder
        self._standard_node_size = 30

        self._max_node_size = self._standard_node_size * 1.5
        self._modifier = 1.1

    def hierarchy(self):
        sizes = []
        for node in self._builder.v_nodes():
            if node.get_type() == "None":
                for n in self._builder.in_edges(node):
                    d = self._builder.get_entity_depth(n.v)
                    if d != 0:
                        break
            else:
                d = self._builder.get_entity_depth(node)
            if d == 0:
                s = self._max_node_size
            else:
                s = int(self._max_node_size / (d * self._modifier))
            sizes.append(s)
        return sizes
        
    def standard(self):
        return [self._standard_node_size for node in self._builder.v_nodes()]

    def class_type(self):
        node_sizes = []
        for node in self._builder.v_nodes():
            if self._builder.get_rdf_type(node) is None:
                node_sizes.append(self._standard_node_size/2)
            else:
                node_sizes.append(self._standard_node_size)
        return node_sizes

    def centrality(self):
        node_sizes = []
        for node in self._builder.v_nodes():
            node_size = 1 + len([*self._builder.in_edges(node)]) + len([*self._builder.out_edges(node)])
            node_size = int((node_size * self._standard_node_size) / 4)
            if node_size > 100:
                node_size = 100
            if node_size < self._standard_node_size/2:
                node_size = self._standard_node_size
            node_sizes.append(node_size)
        return node_sizes

    def in_centrality(self):
        node_sizes = []
        for node in self._builder.v_nodes():
            node_size = 1 + len([*self._builder.in_edges(node)])
            node_size = int((node_size * self._standard_node_size) / 2)
            if node_size > 100:
                node_size = 100
            if node_size < self._standard_node_size/2:
                node_size = self._standard_node_size
            node_sizes.append(node_size)
        return node_sizes

    def out_centrality(self):
        node_sizes = []
        for node in self._builder.v_nodes():
            node_size = 1 + len([*self._builder.out_edges(node)])
            node_size = int((node_size * self._standard_node_size) / 2)
            if node_size > 100:
                node_size = 100
            if node_size < self._standard_node_size/2:
                node_size = self._standard_node_size
            node_sizes.append(node_size)
        return node_sizes


    