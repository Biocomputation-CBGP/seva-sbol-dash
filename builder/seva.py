from builder.abstract import AbstractBuilder
from utility.database.hub_interface import SevaHubInterface
from builder.builders.components import ComponentViewBuilder
from builder.builders.circular import CircularViewBuilder
from utility.payload_insert import add_payload,r_sites
from graphs.sbol_graph import SBOLGraph
class SevaBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self._db_handler = SevaHubInterface()

    def get_restriction_sites(self):
        return list(r_sites.keys())

    def insert_payload(self,payload,start,end):
        payload = SBOLGraph(payload)
        add_payload(self._graph,payload,start,end)

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

    def set_circular_view(self):
        self._view_builder = CircularViewBuilder(self._graph)