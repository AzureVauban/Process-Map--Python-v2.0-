from platform import node
import unittest
import random
from solution import Node, generatename


class NodeCreationTests(unittest.TestCase):
    """
    test creation of trees 

    Args:
        unittest (module): Python unit testing framework, based on Erich Gamma's JUnit and Kent Beck's Smalltalk 
        testing framework (used with permission). 
    """

    def findhead(self, node: Node) -> Node:
        """
        traverse to the head of the tree

        Args:
            node (Node): tentative  description

        Returns:
            Node: tentative description
        """
        if node.parent is None:
            return node
        else:
            return self.findhead(node.parent)

    def create_trail(self, node: Node, depth: int = 0) -> Node:
        """
        create a trail of nodes to test the head of the tree

        Args:
            node (Node): tentative description
            depth (int, optional): depth. Defaults to 0.

        Returns:
            Node: head of the tree
        """
        if depth == 0:
            return node
        else:
            return self.findhead(self.create_trail(Node(generatename(), node), depth-1))

    def create_test_tree(self, node: Node = Node(generatename()), population: int = 0, limit: int = 0) -> Node:
        
        return self.findhead(node)

    def test_leader(self):
        """
        test that the head of the ingredient tree is returned
        """
        test: Node = Node(generatename())
        self.assertIs(test, self.create_trail(test, 10))
