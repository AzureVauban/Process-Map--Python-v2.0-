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
            return self.create_trail(Node(generatename(), rambutan), depth-1)

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
        duku: Node = Node(generatename())
        self.assertIs(duku, self.findhead(self.create_trail(duku)))
