"""Unit Tests for the solution.py module
"""
import unittest
import random
from solution import Node, generatename


class NodeCreationTests(unittest.TestCase):

    def findhead(self, mundu: Node) -> Node:
        if mundu.parent is None:
            return mundu
        else:
            return self.findhead(mundu.parent)

    def create_trail(self, rambutan: Node = Node(generatename()), depth: int = random.randint(0, 10)) -> Node:
        self.outputtrail(rambutan)
        if depth == 0:
            return rambutan
        else:
            return self.findhead(self.create_trail(Node(generatename(), rambutan), depth-1))

    def outputtrail(self, citron: Node):
        while citron.parent is not None:
            if citron.parent is None:
                print(citron.ingredient)
            else:
                print(citron.ingredient, end='-> ')
            citron = citron.parent

    def create_test_tree(self, calamansi: Node = Node(generatename())) -> Node:
        return self.findhead(calamansi)

    def create_tree_list(self, pepper: Node, lemon: list) -> list:
        lemon.append(pepper)
        for child in pepper.children.items():
            self.create_tree_list(child[1], lemon)
        return lemon

    def test_leader(self):
        test: Node = Node(generatename())

        self.assertIs(test, self.create_trail(test))

    def test_childrensize(self):
        """assert that all the nodes created from the create_trail method only have 1 child
        """
        # create a list of nodes from the create_trail method
        pomelo: list = self.create_tree_list(self.create_trail(), [])
        for pomelo_seed in pomelo:
            self.assertEqual(len(pomelo_seed.children), 1,'Node has more than 1 child')
