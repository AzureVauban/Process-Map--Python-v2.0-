import unittest
import random
from solution import Node, generatename


class NodeCreationTests(unittest.TestCase):
    """_summary_

    Args:
        unittest (_type_): _description_
    """

    def returnhead(self, node: Node) -> Node:
        """traverse to the head of the tree

        Args:
            node (Node): tentative 

        Returns:
            Node: tentative
        """
        if node.parent is None:
            return node
        else:
            return self.returnhead(node.parent)

    def create_trail(self, node: Node, depth: int = 0) -> Node:
        """create a trail of nodes to test the head of the tree

        Args:
            node (Node): tentative
            depth (int, optional): depth. Defaults to 0.

        Returns:
            Node: head of the tree
        """
        if depth == 0:
            return node
        else:
            return self.returnhead(self.create_trail(Node(generatename(), node), depth-1))

    def test_leader(self):
        """test that the head of the ingredient tree is returned
        """
        test: Node = Node(generatename())
        self.assertIs(test, self.create_trail(test, 10))
