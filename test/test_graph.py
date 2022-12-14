import unittest
import os
import sys

sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))
sys.path.insert(0, os.path.join("..","..",".."))

from graphs.sbol_graph import SBOLGraph
from utility.payload_insert import add_payload
curr_dir = os.path.dirname(os.path.realpath(__file__))

class TestInsertPayload(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pfn = os.path.join(curr_dir,"files","pSEVA111.xml") 
        self.graph = SBOLGraph(pfn)

    @classmethod
    def tearDownClass(self):
        pass
    
    def test_msc_default(self):
        dfn = os.path.join(curr_dir,"files","nor_full.xml")
        pgraph = SBOLGraph(dfn)
        r_graph = add_payload(self.graph,pgraph,"PacI","SpeI")
        #r_graph = SBOLGraph(res)
        
        #print(len(self.graph),len(pgraph),len(r_graph))
        r_graph.export("tst.xml")
        exit()
        for cd in r_graph.get_component_definitions():
            print(cd)
            for c in r_graph.get_components(cd[1]["key"]):
                print(c)
            print("\n\n\n")
if __name__ == '__main__':
    unittest.main()
