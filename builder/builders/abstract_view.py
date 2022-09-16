import networkx as nx

class AbstractViewBuilder():
    def __init__(self,graph):
        self._graph = graph

    def set_graph(self,graph):
        self._graph = graph

    def _subgraph(self, edges=[], nodes=[],new_graph=None):
        if not new_graph:
            new_graph = nx.MultiDiGraph()
            for n,v,e,d in edges:
                ndata = self._graph.nodes[n]
                vdata = self._graph.nodes[v]
                new_graph.add_node(n,**ndata)
                new_graph.add_node(v,**vdata)
                new_graph.add_edge(n,v,e,**d)
            for n,ndata in nodes:
                new_graph.add_node(n,**ndata)
        return new_graph