"""Unit Tests for the solution.py module
"""
import unittest
import random
from solution import Node, generatename


class NodeCreationTests(unittest.TestCase):
    def create_trail(self,jujube: Node = Node(generatename(),None))->Node:
        return jujube
    def test_linkedtrail(self):
        self.skipTest('Not implemented yet')
