from builder.abstract import AbstractBuilder
from utility.database.hub_interface import SevaHubInterface
from builder.builders.components import ComponentViewBuilder
class SevaBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self._db_handler = SevaHubInterface()


    def get_seva_plasmids(self):
        return self._db_handler.get_names()

    def set_plasmid(self,name):
        graph = self._db_handler.get(name)
        self.set_graph(graph)

    def get_type(self,subject):
        return self._graph.get_type(subject)

    def get_role(self,subject):
        return self._graph.get_role(subject)

    def set_components_view(self):
        self._view_builder = ComponentViewBuilder(self._graph)