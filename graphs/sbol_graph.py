import re
from rdflib import URIRef,Literal,RDF,DCTERMS
from graphs.abstract_graph import AbstractGraph
from utility.sbol_identifiers import identifiers
from pysbolgraph.SBOL2Serialize import serialize_sboll2
from pysbolgraph.SBOL2Graph import SBOL2Graph
from rdflib import Graph

class SBOLGraph(AbstractGraph):
    def __init__(self, graph=None):
        super().__init__(graph)

    def export(self,out):
        g = Graph()
        for n,v,e in self.edges(keys=True):
            nk = self.nodes[n]["key"]
            vk = self.nodes[v]["key"]
            g.add((nk,e[1],vk))
        pysbolG = SBOL2Graph()
        pysbolG += g
        with open(out, 'w') as o:
            o.write(serialize_sboll2(pysbolG).decode("utf-8"))

    def remove_sa(self,sa):
        for l in self.get_locations(sa=sa):
            self.remove_node(l[0])
        for c in self.get_components(sa=sa):
            definition = self.get_definition(c[0])
            seq = self.get_sequence(definition[0])
            if seq is not None and len(self.search((None,identifiers.predicates.sequence,seq[0]))) == 1:
                self.remove_node(seq[0])
            for sc in self.get_sequence_constraints(c=c[0]):
                try:
                    self.remove_node(sc[0])
                except Exception:
                    pass
            self.remove_node(definition[0])
            self.remove_node(c[0])

        self.remove_node(sa)


    def remove_edge(self,edge):
        pass

    def replace_sequence(self,subject,new):
        seq_s = self.search((subject,identifiers.predicates.sequence,None),lazy=True)[1][1]["key"]
        seq_n = self.search((seq_s, identifiers.predicates.elements, None),lazy=True)[1][0]
        self.nodes[seq_n]["key"] = Literal(new)
        
    def replace(self,identifier,new_k):
        self.nodes[identifier]["key"] = new_k

    def get_root(self):
        r = [cd for cd in self.get_component_definitions() if self.get_heirachy_instances(cd[1]["key"]) == []]
        assert(len(r) == 1)
        return r[0]

    def get_root_sequence(self):
        root = [cd for cd in self.get_component_definitions() if self.get_heirachy_instances(cd[1]["key"]) == []]
        assert(len(root) == 1)
        return self.get_sequence(root[0][1]["key"])

    def get_rdf_type(self, subject):
        definition = self.search(
            (subject, identifiers.predicates.rdf_type, None), lazy=True)
        if definition != []:
            return definition[1]


    def get_sequence(self,cd):
        seq_o = self.search((cd,identifiers.predicates.sequence,None),lazy=True)
        if seq_o == []:
            return None
        seq_o = seq_o[1][1]
        return self.search((seq_o["key"],identifiers.predicates.elements,None),lazy=True)[1]

    def get_component_definitions(self):
        return [cd[0] for cd in self.search((None, identifiers.predicates.rdf_type,
                                             identifiers.objects.component_definition))]

    def get_component_instances(self):
        return self.search((None, [identifiers.predicates.component,
                                   identifiers.predicates.functional_component], None))

    def get_module_definitions(self):
        return [md[0] for md in self.search((None, identifiers.predicates.rdf_type,
                                            identifiers.objects.module_definition))]

    def get_definition(self, component):
        definition = self.search(
            (component, identifiers.predicates.definition, None), lazy=True)
        if definition != []:
            return definition[1]

    def get_type(self, subject):
        r_type = self.search(
            (subject, identifiers.predicates.type, None), lazy=True)
        if r_type != []:
            return r_type[1]

    def get_role(self, subject):
        role = self.search(
            (subject, identifiers.predicates.role, None), lazy=True)
        if role != []:
            return role[1]

    def get_types(self, subject):
        return [t[1] for t in self.search((subject, identifiers.predicates.type, None))]

    def get_roles(self, subject):
        return [t[1] for t in self.search((subject, identifiers.predicates.role, None))]

    def get_participations(self, interaction):
        return [i[1] for i in self.search((interaction, identifiers.predicates.participation, None))]

    def get_sequence_annotations(self, cd=None,loc=None):
        if cd is not None:
            return [sa[1] for sa in self.search((cd, identifiers.predicates.sequence_annotation, None))]
        if loc is not None:
            return [sa[0] for sa in self.search((None, identifiers.predicates.location, loc))]
        else:
            return [sa[1] for sa in self.search((None, identifiers.predicates.sequence_annotation, None))]

    def get_sa(self,c): 
        return [sa[0] for sa in self.search((None, identifiers.predicates.component, c)) if 
        self.search((sa[0][1]["key"], identifiers.predicates.rdf_type, identifiers.objects.sequence_annotation)) != []]

    def get_sequence_constraints(self, cd=None,c=None):
        if cd is not None:
            return [sc[1] for sc in self.search((cd, identifiers.predicates.sequence_constraint, None))]
        if c is not None:
            return [sc[0] for sc in self.search((None, [identifiers.predicates.sequence_constraint_subject,identifiers.predicates.sequence_constraint_object], None))]

    def get_locations(self, sa=None,range=None):
        if sa is not None:
            return [l[1] for l in self.search((sa, identifiers.predicates.location, None))]
        elif range is not None:
            return [l[0] for l in self.search((None,[identifiers.predicates.start,identifiers.predicates.end], range))]
            
    def get_components(self, cd=None, sa=None):
        if cd is not None:
            s = cd
        elif sa is not None:
            s = sa
        else:
            s = None
        return [c[1] for c in self.search((s, identifiers.predicates.component, None))]

    def get_modules(self, md=None):
        if md is not None:
            s = md
        return [c[1] for c in self.search((s, identifiers.predicates.module, None))]

    def get_interactions(self, md=None):
        return [i[1] for i in self.search((md, identifiers.predicates.interaction, None))]

    def get_functional_components(self, md=None):
        return [fc[1] for fc in self.search((md, identifiers.predicates.functional_component, None))]

    def get_component_definition(self, participation=None):
        if participation is not None:
            fc = self.search(
                (participation, identifiers.predicates.participant, None), lazy=True)
            if fc is None:
                return None
            fc = fc[1][1]["key"]
            cd = self.get_definition(fc)
            return cd

    def get_heirachy_instances(self, cd=None):
        return [c[0] for c in self.search((None, identifiers.predicates.definition, cd))]

    def get_top_levels(self):
        return [tl[0] for tl in self.search((None, identifiers.predicates.rdf_type, identifiers.objects.top_levels))]

    def get_maps_to(self, md=None):
        return [m[1] for m in self.search((md, identifiers.predicates.maps_to, None))]

    def get_property(self, subject, predicate):
        return [p[1] for p in self.search((subject, predicate, None))]

    def _generic_generation(self,uri,type):
        if not isinstance(uri,URIRef):
            uri = URIRef(uri)
        triples = [(uri,RDF.type,type)]
        triples.append((uri,identifiers.predicates.persistent_identity,_get_pid(uri)))
        triples.append((uri,identifiers.predicates.display_id,Literal(_get_name(uri))))
        triples.append((uri,identifiers.predicates.version,Literal(1)))
        return triples

    def add_sequence(self,uri,sequence,encoding):
        triples = self._generic_generation(uri,identifiers.objects.sequence)
        triples.append((uri,identifiers.predicates.elements,sequence))
        triples.append((uri,identifiers.predicates.encoding,encoding))
        self.add_new_edges(triples)
        
    def add_component_definition(self,uri,type,role=None,components=[],sas=[],properties={}):
        if not isinstance(uri,URIRef):
            uri = URIRef(uri)
        triples = self._generic_generation(uri,identifiers.objects.component_definition)
        triples.append((uri,identifiers.predicates.type,type))
        if role is not None:
            triples.append((uri,identifiers.predicates.role,role))
        for component in components:
            triples.append((uri,identifiers.predicates.component,URIRef(component)))
        
        for sa in sas:
            triples.append((uri,identifiers.predicates.sequence_annotation,URIRef(sa)))
        properties[DCTERMS.title] = Literal(_get_name(uri))

        for k,v in properties.items():
            triples.append((uri,k,v))
        self.add_new_edges(triples)

    def add_component(self,uri,definition,parent=None):
        triples = self._generic_generation(uri,identifiers.objects.component)
        triples.append((uri,identifiers.predicates.definition,definition))
        triples.append((uri,identifiers.predicates.access,identifiers.external.component_instance_acess_public))
        if parent is not None:
            triples.append((parent,identifiers.predicates.component,uri))
        self.add_new_edges(triples)

    def add_module_definition(self,uri,modules,interactions):
        uri = self.create_md_name(uri)
        triples = self._generic_generation(uri,identifiers.objects.module_definition)
        for module in modules:
            module = URIRef(module)
            definition = self.create_md_name(module)
            m_uri = self.build_children_uri(uri,module)
            triples += self.module(m_uri,definition)
            triples.append((uri,identifiers.predicates.module,m_uri))
        for i,(i_type,parts,props) in interactions.items():
            interaction = self.build_children_uri(uri,i)
            triples.append((uri,identifiers.predicates.interaction,interaction))
            participants = {}
            for cd,part_type in parts.items():
                cd_key = URIRef(cd.get_key())
                fc = self.create_fc_name(uri,cd_key)
                cd.key = fc
                triples += self.functional_component(fc,cd_key)
                triples.append((uri,identifiers.predicates.functional_component,fc))
                participants[cd] = part_type
            triples += self.interaction(interaction,i_type,participants,props)
        self.add_new_edges(triples)


    def add_module(self,uri,definition):
        triples = self._generic_generation(uri,identifiers.objects.module)
        triples.append((uri,identifiers.predicates.definition,definition))
        self.add_new_edges(triples)

    def add_interaction(self,uri,type,parts,properties={}):
        triples = self._generic_generation(uri,identifiers.objects.interaction)
        triples.append((uri,identifiers.predicates.type,type))
        for fc,part_type in parts.items():
            part = self.create_part_name(uri,fc.get_key(),fc.get_type())
            triples += self.participation(part,fc.get_key(),part_type)
            triples.append((uri,identifiers.predicates.participation,part))
        for k,v in properties.items():
            triples.append((uri,k,v))
        self.add_new_edges(triples)

    def add_participation(self,uri,fc,part_type):
        triples = self._generic_generation(uri,identifiers.objects.participation)
        triples.append((uri,identifiers.predicates.role,part_type))
        triples.append((uri,identifiers.predicates.participant,URIRef(fc)))
        self.add_new_edges(triples)

    def add_functional_component(self,uri,definition):
        triples = self._generic_generation(uri,identifiers.objects.functional_component)
        triples.append((uri,identifiers.predicates.definition,URIRef(definition)))
        triples.append((uri,identifiers.predicates.access,identifiers.objects.public))
        triples.append((uri,identifiers.predicates.direction,identifiers.objects.inout))
        self.add_new_edges(triples)

    def add_sequence_annotation(self,uri,start,end,strand,parent,component=None):
        triples = self._generic_generation(uri,identifiers.objects.sequence_annotation)
        r_uri = self.build_children_uri(uri,f'{uri[0:-2]}_range/1')
        triples += self.range(r_uri,start,end,strand)
        triples.append((uri,identifiers.predicates.location,r_uri))
        triples.append((uri,URIRef("http://wiki.synbiohub.org/wiki/Terms/synbiohub#topLevel"),parent))
        if component is not None:
            triples.append((uri,identifiers.predicates.component,component))
        self.add_new_edges(triples)

    def add_range(self,uri,start,end,strand):
        triples = self._generic_generation(uri,identifiers.objects.range)
        triples.append((uri,identifiers.predicates.start,start))
        triples.append((uri,identifiers.predicates.end,end))
        triples.append((uri,identifiers.predicates.orientation,strand))
        self.add_new_edges(triples)

    def build_children_uri(self,base,addition):
        return URIRef(f'{_get_pid(base)}/{_get_name(addition)}/1')

    def create_md_name(self,uri):
        return URIRef(f'{_get_pid(uri)}_md/1')

    def create_sequence_name(self,uri):
        return URIRef(f'{_get_pid(uri)}_sequence/1')

    def create_component_name(self,cd):
        return URIRef(self.build_children_uri(cd,_get_name(cd)+"_c"))

    def create_part_name(self,int,cd,part_type): # Part type is CD type.
        return URIRef(self.build_children_uri(int,f'{_get_name(cd)}_{_get_name(part_type)}'))

def _get_pid(subject):
    if subject[-1].isdigit():
        return URIRef(subject[:-2])

def _get_name(subject):
    split_subject = _split(subject)
    if len(split_subject) == 1:
        return subject
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