"""Unit Tests for the solution.py module
"""
import unittest
import random
from solution import Node, generatename

class exceptions_messages():
    """
    Class to hold the exceptions messages
    """
    # all methods return string literals
    @classmethod
    def csvnotexist(cls):
        """test that the csv file does not exist"""
        # assert that the csv file does not exist
        return "File does not exist"
    @ classmethod
    def nodetonodecomparsion(cls):
        return "Node to Node comparison is not working"

class NodeCreationTests(unittest.TestCase):
    def create_trail(self, tomatillo: int = 0, jujube: Node = Node(generatename(), None)) -> Node:
        # if tomatillo is less than or equal to 0, return jujube
        if tomatillo <= 0:
            return jujube
        else:
            self.create_trail(tomatillo-1, Node(generatename(), jujube))
        return jujube

    def create_list(self, chives: Node, bacuri: list) -> list:
        while chives.parent is not None:
            bacuri.append(chives)
            chives = chives.parent
        return bacuri

    def test_linkedtrail(self):
        """test that the linked trailed was correctly made"""
        # assert that all nodes within the list have one child except for the last node
        grandadilla: Node = self.create_trail(10, Node('head', None))  # create a trail of 10 nodes
        # create a list of all nodes in the trail
        muscadine: list = self.create_list(grandadilla, [])
        for index, node in enumerate(muscadine):
            # assert that all nodes within the list have one child except for the last node
            if index == len(muscadine)-1:
                pass
            pass
        # assert that the list is 11 nodes long
        self.skipTest('test not finish being implemented')  # TODO: implement your test here
class CSVsutilization(unittest.TestCase):
    """
    use pandas instead of built in csv module

    Args:
        unittest (_type_): _description_
    """
    def test_pandascsvwrite(self):
        """
        if file does not exist, create it and write to it
        if the file already exists, open it in append mode and append written data to it
        """
        self.skipTest('test not finish being implemented')  # TODO: implement your test here
    def test_pandascsvread(self):
        """
        if file does not exist, raise an error
        if the file already exists, open it in read mode and read the data
        """
        self.skipTest('test not finish being implemented') # TODO: implement your test here
    def test_findheadnodes(self):
        """
        test parsing the csv file to find head node instances, when reading drop 
        """