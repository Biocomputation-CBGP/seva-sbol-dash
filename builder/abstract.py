import re
import networkx as nx
from graphs.sbol_graph import SBOLGraph
from builder.builders.full import FullViewBuilder

class AbstractBuilder:
    def __init__(self):
        self._graph = SBOLGraph()
        self.view = nx.MultiDiGraph()
        self._view_builder = FullViewBuilder(self._graph)

    def set_full_view(self):
        self._view_builder = FullViewBuilder(self._graph)

    def set_graph(self,graph):
        self._graph = SBOLGraph(graph)

    def build(self,*args,**kwargs):
        self.view = self._view_builder.build(*args,**kwargs)
        
    def get_rdf_type(self,subject):
        return self._graph.get_rdf_type(subject)

    def get_view_nodes(self, identifier=None):
        return self.view.get_node(identifier)
        
    def v_nodes(self,**kwargs):
        return self.view.nodes(**kwargs)

    def v_edges(self,n=None,**kwargs):
        return self.view.edges(n,**kwargs)

    def in_edges(self, n=None,**kwargs):
        return self.view.in_edges(n,**kwargs)

    def out_edges(self, n=None,**kwargs):
        return self.view.out_edges(n,**kwargs)
        
    def get_namespace(self, uri):
        split_subject = _split(uri)
        if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
            name = split_subject[-2]
        else:
            name = split_subject[-1]
        return uri.split(name)[0]

def _split(uri):
    return re.split('#|\/|:', uri)
