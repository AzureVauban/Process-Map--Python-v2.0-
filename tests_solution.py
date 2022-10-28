"""
Unit Tests for the solution.py module
"""
import os
import unittest
import random
from solution import Node, generatename, createclone
from solution import FIELDNAMES
TESTFILENAME: str = "tests_solution.csv"


class exep_msg():
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

    @classmethod
    def testnotadded(cls):
        return "Test not implemented"
    @classmethod
    def headisNone(cls):
        return "head of the tree is None"
class NodeTree:
        """
        auto generated a tree of nodes
        """
        headnode: Node
        population: int = 1

        def generateTree(self, populationlimt: int = 1, head: Node = Node('head', None)) -> Node:
            if head is None:
                raise ValueError(exep_msg.headisNone())
            return head
        def __init__(self, population: int = 1):
            self.generateTree(population)
class NodeCreationTests(unittest.TestCase):

    def testcheckclone(self):
        """
        test that the clone is created correctly
        """
        tomato: Node = Node('tomato')
        tomahto = createclone(tomato)
        self.assertIsNot(tomato, tomahto, 'Clone is not at a unique location')


class internalsearch(unittest.TestCase):
    
    def test_search(self):
        """
        assert that return dict from the search method is {-1:None}
        """
        ingredientname: str = generatename()
        nodetree = Node()   # create a node tree
        self.skipTest(exep_msg.testnotadded())  # skip the test


class CSVsutilization(unittest.TestCase):
    """
    @note use pandas instead of built in csv module

    Args:
        unittest (_type_): _description_
    """
    # @audit-info use df.iloc to read an entire row of data
    # @audit-info use df.columns to read the column names
    # @audit-info use df.iterrows to iterate through the rows of the dataframe (dataframe referred to as df and the csvfile)

    def test_pandascsvwrite(self):
        """
        if file does not exist in the SAME directory as the solution module, create it and write to it
        if the file already exists, open it in append mode and append written data to it
        """
        if not os.path.exists(TESTFILENAME):
            # create the file
            # write preset mock ingredient tree onto it
            pass
        # TODO: implement your test here
        self.skipTest(exep_msg.testnotadded())

    def test_pandascsvread(self):
        """
        if file does not exist, raise an error
        if the file already exists, open it in read mode and read the data
        """
        if not os.path.exists(TESTFILENAME):
            raise FileNotFoundError(exep_msg.csvnotexist())
        # TODO: implement your test here
        self.skipTest(exep_msg.testnotadded())

    def test_findheadnodes(self):
        """
        test parsing the csv file to find head node instances
        """
        # TODO: implement your test here
        self.skipTest(exep_msg.testnotadded())


if __name__ == '__main__':
    unittest.main()
