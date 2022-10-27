import unittest
import random
from solution import Node,generatename


class NodeCreationTests(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def create_trail(self,node : Node,depth : int = 0) ->Node:
        if depth == 0:
            return node
        else:
            return self.create_trail(Node(generatename(),node),depth-1)
    def returnhead(self, node : Node) -> Node:
        if node.parent is None:
            return node
        else:
            return self.returnhead(node.parent)
    def test_leader(self):
        """test that the head of the ingredient tree is returned
        """
        test : Node = Node(generatename())
        assertNode : Node = self.create_trail(test,10)
        self.assertEqual(test,assertNode)