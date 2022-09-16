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
        dfn = os.path.join(curr_dir,"files","nor_full.xml") #Bad Example
        pgraph = SBOLGraph(dfn)
        add_payload(self.graph,pgraph,"PacI","SpeI")
            
if __name__ == '__main__':
    unittest.main()
