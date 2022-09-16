import dash_cytoscape as cyto
cyto.load_extra_layouts()
from visual.abstract import AbstractVisual

from visual.abstract import AbstractVisual
from builder.seva import SevaBuilder

class SevaVisual(AbstractVisual):
    def __init__(self):
        super().__init__(SevaBuilder())

    def get_seva_plasmids(self):
        return self._builder.get_seva_plasmids()
    
    def set_plasmid(self,name):
        self._builder.set_plasmid(name)

    def set_component_graph_view(self):
        '''
        Renders the Full graph. 
        '''
        if self.view == self.set_component_graph_view:
            self._builder.set_components_view()
        else:
            self.view = self.set_component_graph_view

        
