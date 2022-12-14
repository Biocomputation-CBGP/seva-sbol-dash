from rdflib import Literal
from utility.sbol_identifiers import identifiers
from Bio.Seq import Seq
from Bio import Restriction
import re

r_sites = {"PacI": Restriction.PacI,
           "hindIII": Restriction.HindIII,
           "PstI": Restriction.XbaI,
           "BamHI": Restriction.BamHI,
           "SmaI": Restriction.SmaI,
           "KpnI": Restriction.KpnI,
           "SacI": Restriction.SalI,
           "EcoRI": Restriction.EcoRI,
           "SfiI": Restriction.SfiI,
           "SphI": Restriction.SphI,
           "AvrII": Restriction.AvrII,
           "SpeI": Restriction.SpeI,
           "SanDI": Restriction.SanDI,
           "NotI": Restriction.NotI}

def restriction_sites(seq, recog_seq):
    """Find the indices of all restriction sites in a sequence."""
    sites = []
    for site in re.finditer(recog_seq, seq):
        sites.append(site.start())

    return sites

def add_payload(vgraph, p_graph,rs_s,rs_e):
    def _get(subject, func):
        i = func(subject[1]["key"])
        assert(len(i) == 1)
        return i[0]

    def _get_prop(subj, prop,graph):
        i = graph.get_property(subj[1]["key"], prop)
        assert(len(i) == 1)
        return i[0]

    root = vgraph.get_root()[1]["key"]
    r_seq = vgraph.get_sequence(root)[1]["key"]
    cds = vgraph.get_component_definitions()
    # Find T0 Terminator + T1 Terminator.
    t0 = None
    for cd in cds:
        if "t0" in cd[1]["key"].lower():
            t0 = cd
            break
    else:
        raise ValueError("Plasmid doesn't have T0 or T1 terminators.")

    t0_c = _get(t0, vgraph.get_heirachy_instances)
    t0_sa = _get(t0_c, vgraph.get_sa)
    t0_l = _get(t0_sa, vgraph.get_locations)
    t0_l_s = _get_prop(t0_l, identifiers.predicates.start,vgraph)
    t0_l_s = int(t0_l_s[1]["key"])

    p_seq = Seq(r_seq[0:t0_l_s-1])
    rs_s_i = restriction_sites(str(p_seq),r_sites[rs_s].site)
    rs_e_i = restriction_sites(str(p_seq),r_sites[rs_e].site)
    if rs_s_i == []:
        raise ValueError(f'{rs_s} Restriction site not in cargo.')
    if rs_e_i == []:
        raise ValueError(f'{rs_e} Restriction site not in cargo.')
    
    rs_s_i = rs_s_i[0] + len(r_sites[rs_s].site) 
    rs_e_i = rs_e_i[0]

    # Update Sequences & annotations.
    p_root = p_graph.get_root()[1]["key"]
    pl_seq = _get_payload_sequence(p_root,p_graph)
    # Get Sequence of payload and insert it inbetween rs_si and rs_e_i
    # Add the rest of the plasmid onto the end of sequence.
    new_root_sequence = p_seq[0:rs_s_i] + pl_seq + p_seq[rs_e_i:] + r_seq[t0_l_s-1:]
    vgraph.replace_sequence(root,new_root_sequence)
    # Plasmid Annotations += Len(design) on all past T0
    for sa in vgraph.get_sequence_annotations():
        loc = _get(sa, vgraph.get_locations)
        start = _get_prop(loc, identifiers.predicates.start,vgraph)
        if int(start[1]["key"]) >= int(t0_l_s):
            n_start = Literal(start[1]["key"] + len(pl_seq))
            vgraph.replace(start[0],n_start)
            end = _get_prop(loc, identifiers.predicates.end,vgraph)
            n_end = Literal(end[1]["key"] + len(pl_seq))
            vgraph.replace(end[0],n_end)
        else:
            vgraph.remove_sa(sa[0])
    # Design += len(rs_s_i)
    for sa in p_graph.get_sequence_annotations():
        loc = _get(sa, p_graph.get_locations)

        start = _get_prop(loc, identifiers.predicates.start,p_graph)
        n_start = Literal(int(start[1]["key"]) + rs_s_i)
        p_graph.replace(start[0],n_start)

        end = _get_prop(loc, identifiers.predicates.end,p_graph)
        n_end = Literal(int(end[1]["key"]) + rs_s_i)
        p_graph.replace(end[0],n_end)

    c_name = p_graph.create_component_name(p_root)
    vgraph.add_component(c_name,p_root,root)
    vgraph.add_graph(p_graph)
    return vgraph

    
def _get_payload_sequence(root,graph):
    p_seq = graph.get_sequence(root)
    if p_seq is None:
        raise NotImplementedError("Need to build the sequence up...")
    return p_seq[1]["key"]
