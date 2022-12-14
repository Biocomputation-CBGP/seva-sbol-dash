from ast import In
from collections import OrderedDict

from dash.dependencies import Input, Output, State

id_prefix = "cyto"
graph_id = "full_graph"
preset_i = OrderedDict()
preset_o = OrderedDict()

# -- Load Plasmid --
lp_i = Input("lp_submit", "n_clicks")
lp_s = State("lp_name", "value")
lp_o = Output("lp_content", "children")

# -- Load Design --
ld_i = Input("ld_submit", "n_clicks")
ld_s = {"sbol":State("ld_name", "value"),
        "start" : State("start_rs","value"),
        "end" : State("end_rs","value")}

# -- Update -- 
update_i = OrderedDict()
update_o = {"graph_id": Output("content", "children"),
            "legend_id": Output("sidebar-right", "children")}






