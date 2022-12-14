import networkx as nx
import re
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



    def _create_edge_dict(self, key, weight=1):
        edge = {'weight': weight,
                'display_name': self._get_name(str(key[1]))}
        return edge

    def _get_name(self, subject):
        split_subject = self._split(subject)
        if len(split_subject) == 1:
            return subject
        if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
            return split_subject[-2]
        elif len(split_subject[-1]) == 3 and _isfloat(split_subject[-1]):
            return split_subject[-2]
        else:
            return split_subject[-1]

    def _split(self, uri):
        return re.split('#|\/|:', uri)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False