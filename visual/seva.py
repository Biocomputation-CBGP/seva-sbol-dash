import os
import dash_cytoscape as cyto
import uuid
cyto.load_extra_layouts()
from visual.abstract import AbstractVisual

from visual.abstract import AbstractVisual
from builder.seva import SevaBuilder

class SevaVisual(AbstractVisual):
    def __init__(self):
        super().__init__(SevaBuilder())

    def get_restriction_sites(self):
        return self._builder.get_restriction_sites()

    def get_seva_plasmids(self):
        return self._builder.get_seva_plasmids()
    
    def set_plasmid(self,name):
        self._builder.set_plasmid(name)

    def add_payload(self,payload,start,end):
        fn = str(uuid.uuid4())+".xml"
        with open(f'{fn}', 'w') as f:
            f.write(payload)
        try:
            self._builder.insert_payload(fn,start,end)
        except Exception as ex:
            os.remove(fn)
            raise ex
        os.remove(fn)

    def set_component_graph_view(self):
        if self.view == self.set_component_graph_view:
            self._builder.set_components_view()
        else:
            self.view = self.set_component_graph_view

    def set_circular_graph_view(self):
        if self.view == self.set_circular_graph_view:
            self._builder.set_circular_view()
        else:
            self.view = self.set_circular_graph_view

        
