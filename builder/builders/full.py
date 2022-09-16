from builder.builders.abstract_view import AbstractViewBuilder
class FullViewBuilder(AbstractViewBuilder):
    def __init__(self,graph):
        super().__init__(graph)

    def _subgraph(self, edges=[], nodes=[],new_graph=None):
        return super()._subgraph(edges,nodes,new_graph)
        
    def build(self):
        edges = self._graph.edges(keys=True,data=True)
        return self._subgraph(edges)