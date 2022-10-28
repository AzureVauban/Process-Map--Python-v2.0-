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

    def create_trail(self, rambutan: Node, depth: int = random.randint(0, 10)) -> Node:
        self.outputtrail(rambutan)
        if depth == 0:
            return rambutan
        else:
            return self.findhead(self.create_trail(Node(generatename(), rambutan), depth-1))
    def outputtrail(self,citron : Node):
        while citron.parent is not None:
            if citron.parent is not None:
                print(citron.ingredient,end='-> ')
            else:
                print(citron.ingredient)
            citron = citron.parent
        
        
    def create_test_tree(self, calamansi: Node = Node(generatename())) -> Node:
        return self.findhead(calamansi)

    def test_leader(self):
        test: Node = Node(generatename())
        #self.outputtrail(test)
        self.assertIs(test, self.create_trail(test))
