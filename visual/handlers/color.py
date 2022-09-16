import re

from visual.handlers.color_producer import ColorPicker
from utility.sbol_identifiers import identifiers

color_picker = ColorPicker()
class ColorHandler:
    def __init__(self,builder):
        self.node = NodeColorHandler(builder)
        self.edge = EdgeColorHandler(builder)

class NodeColorHandler:
    def __init__(self,builder):
        self._builder = builder
        self._color_picker = color_picker
    
    def standard(self):
        return [{"standard" : self._color_picker[0]} for node in self._builder.v_nodes()]

    def rdf_type(self):
        colors = []
        for node in self._builder.v_nodes():
            nt = self._builder.get_rdf_type(node)
            if nt is None:
                color = {"rdf_type" : self._color_picker[0]}
            else:
                color = {"no_type" : self._color_picker[1]}
            colors.append(color)
        return colors

    def type(self):
        colors = []
        col_map = {None : {"No_Type" : self._color_picker[0]}}
        col_index = len(col_map)
        for n in self._builder.v_nodes():
            n_type = self._builder.get_rdf_type(n)
            if n_type is None:
                colors.append(col_map[None])
            else:
                name = _get_name(n_type[1]["key"])
                if name not in col_map.keys():
                    col_map[name] = self._color_picker[col_index]
                    col_index += 1
                colors.append({name : col_map[name]})
        return colors


    def role(self):
        colors = []
        col_index = 1
        col_map = {None : {"No_Role" : self._color_picker[0]}}
        for node,data in self._builder.v_nodes(data=True):
            node_type = self._builder.get_type(node)
            node_role = self._builder.get_role(node)
            if node_role is not None:
                node_role = node_role[1]["key"]
                node_role_name = self._translate_role(node_role)
                if node_role_name not in col_map:
                    col_map[node_role_name] = color_picker[col_index]
                    col_index +=1
                colors.append({node_role_name : col_map[node_role_name]})
                continue
            if node_type is not None:
                node_type = node_type[1]["key"]
                node_type_name = self._translate_role(node_type)
                if node_type_name not in col_map:
                    col_map[node_type_name] = color_picker[col_index]
                    col_index +=1
                colors.append({node_type_name : col_map[node_type_name]})
                continue
            colors.append(col_map[None])
            continue

        return colors


    def _translate_role(self,identifier):
        node_type_name = identifiers.translate_role(identifier)
        if node_type_name is None:
            node_type_name = _get_name(identifier)
        node_type_name = node_type_name.replace(" ","_").lower()
        return node_type_name

class EdgeColorHandler:
    def __init__(self,builder):
        self._builder = builder
        self._color_picker = color_picker

    def standard(self):
        return [{"standard" : "#888"} for e in self._builder.v_edges()]
    
    def type(self):
        colors = []
        col_map = {}
        col_index = 0
        for n,v,e in self._builder.v_edges(keys=True):
            edge = _get_name(e[1])
            if edge not in col_map:
                col_map[edge] = self._color_picker[col_index]
                col_index +=1
            colors.append({edge:col_map[edge]})
        return colors
    

def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject[-1]) == 1 and split_subject[-1].isdigit():
        return split_subject[-2]
    elif len(split_subject[-1]) == 3 and _isfloat(split_subject[-1]):
        return split_subject[-2]
    else:
        return split_subject[-1]

def _split(uri):
    return re.split('#|\/|:', uri)

def _isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False