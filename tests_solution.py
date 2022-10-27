import unittest
import random
from solution import Node,generatename


class NodeCreationTests(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def create_trail(self,node : Node,depth : int = 0):
        if depth == 0:
            return node
        else:
            self.create_trail(Node(generatename(),node),depth-1)
            
    def test_leader(self):
        """test that the head of the ingredient tree is returned
        """
        #!self.skipTest('Not implemented yet')