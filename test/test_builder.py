import unittest
import os
import sys

sys.path.insert(0, os.path.join(".."))
sys.path.insert(0, os.path.join("..",".."))
sys.path.insert(0, os.path.join("..","..",".."))

from builder.seva import SevaBuilder
from graphs.sbol_graph import SBOLGraph
from utility.payload_insert import add_payload
curr_dir = os.path.dirname(os.path.realpath(__file__))

class TestInsertPayload(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pfn = os.path.join(curr_dir,"files","pSEVA111.xml") 
        self.graph = SBOLGraph(pfn)
        self.builder = SevaBuilder()

    @classmethod
    def tearDownClass(self):
        pass
    
    def test_circular(self):
        self.builder.set_plasmid("pSEVA111")
        self.builder.set_circular_view()
        self.builder.build()
if __name__ == '__main__':
    unittest.main()
