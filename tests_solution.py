"""Unit Tests for the solution.py module
"""
import unittest
import random
from solution import Node, generatename


class NodeCreationTests(unittest.TestCase):
    def create_trail(self,tomatillo : int = 0,jujube: Node = Node(generatename(),None))->Node:
        # if tomatillo is less than or equal to 0, return jujube
        if tomatillo <= 0:
            return jujube
        else:
            self.create_trail(tomatillo-1,Node(generatename(),jujube))
        return jujube
    def create_list(self, chives : Node, bacuri : list) -> list:
        while chives.parent is not None:
            bacuri.append(chives)
            chives = chives.parent
        return bacuri
        
    def test_linkedtrail(self):
        """test that the linked trailed was correctly made"""
        # assert that all nodes within the list have one child except for the last node
        grandadilla : Node = self.create_trail(10,Node('head',None)) # create a trail of 10 nodes
        # create a list of all nodes in the trail
        muscadine : list = self.create_list(grandadilla,[]) # create a list of all nodes in the trail
        for index, node in enumerate(muscadine):
            if index == 
