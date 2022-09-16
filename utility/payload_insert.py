from utility.sbol_identifiers import identifiers
from Bio.Seq import Seq
from Bio import Restriction

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


def add_payload(vgraph, p_graph,rs_s,rs_e):
    def _get(subject, func):
        i = func(subject[1]["key"])
        assert(len(i) == 1)
        return i[0]

    def _get_prop(subj, prop):
        i = vgraph.get_property(subj[1]["key"], prop)
        assert(len(i) == 1)
        return i[0]

    root = vgraph.get_root()
    r_seq = vgraph.get_sequence(root[1]["key"])[1]["key"]
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
    t0_l_s = _get_prop(t0_l, identifiers.predicates.start)
    t0_l_s = int(t0_l_s[1]["key"])

    p_seq = Seq(r_seq[0:t0_l_s-1])

    print(p_seq)
    rs_s_i = r_sites[rs_s].search(p_seq)
    rs_e_i = r_sites[rs_e].search(p_seq)
    if rs_s_i == []:
        raise ValueError(f'{rs_s} Restriction site not in cargo.')
    if rs_e_i == []:
        raise ValueError(f'{rs_e} Restriction site not in cargo.')


    p_root = p_graph.get_root()[1]["key"]
    # Create component
    c_name = p_graph.create_component_name(p_root)
    p_graph.add_component(c_name,p_root)

    print(rs_s,rs_e)

    

