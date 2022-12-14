from builder.builders.abstract_view import AbstractViewBuilder
from utility.sbol_identifiers import identifiers
import operator
class CircularViewBuilder(AbstractViewBuilder):
    def __init__(self,graph):
        super().__init__(graph)

    def _subgraph(self, edges=[], nodes=[],new_graph=None):
        return super()._subgraph(edges,nodes,new_graph)
        
    def build(self):
        edges = []
        starts = []
        for sa in self._graph.get_sequence_annotations():
            loc = self._graph.get_locations(sa[1]["key"])[0]
            start = self._graph.get_property(loc[1]["key"],identifiers.predicates.start)
            comp = self._graph.get_components(sa=sa[1]["key"])
            if comp != []:
                sa = self._graph.get_definition(comp[0][1]["key"])
            starts.append((sa[0],int(start[0][1]["key"])))
        sorted_d = sorted(starts, key=lambda tup: tup[1])
        for index,(k,v) in enumerate(sorted_d):
            if index == len(sorted_d) -1:
                edges.append((k,sorted_d[0][0],"hasPart",self._create_edge_dict("hasPart")))
            else:
                edges.append((k,sorted_d[index+1][0],"hasPart",self._create_edge_dict("hasPart")))
        return self._subgraph(edges)