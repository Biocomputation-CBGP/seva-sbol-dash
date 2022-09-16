from builder.builders.abstract_view import AbstractViewBuilder
class ComponentViewBuilder(AbstractViewBuilder):
    def __init__(self,graph):
        super().__init__(graph)

    def _subgraph(self, edges=[], nodes=[],new_graph=None):
        return super()._subgraph(edges,nodes,new_graph)
        
    def build(self):
        edges = []
        for cd in self._graph.get_component_definitions():
            for component in self._graph.get_components(cd[0]):
                definition = self._graph.get_definition(component[0])
                edges.append((cd[0],definition[0],"hasPart",{}))
        return self._subgraph(edges)