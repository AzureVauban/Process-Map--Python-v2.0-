"""
Unit Tests for the solution.py module
"""
import os
import unittest
import random
import pandas
from solution import Node, generatename, createclone, reversearithmetic
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

    def testsubstringmethod(self):
        # reformat a string to have all of its whitespace turn into an underscore
        teststring: str = 'this is a test string'  # test string
        teststring = teststring.strip()
        # replace all whitespace with underscores
        teststring = teststring.replace(' ', '_')
#!        self.assertEqual(teststring, 'this_is_a_test_string')  # assert that the string is formatted correctly
        self.skipTest('Test is not needed anymore')  # skip the test

    def test_pandascsvwrite(self):
        """
        if file does not exist in the SAME directory as the solution module, create it and write to it
        if the file already exists, open it in append mode and append written data to it
        """
        # prepared mock ingredient append data
        industrial_battery    : Node = Node('industrial battery', None)
        protocite_bar         : Node = Node('protocite bar', industrial_battery, 0, 1, 5)
        protocite             : Node = Node('protocite', protocite_bar, 0, 1, 2)
        battery               : Node = Node('battery', industrial_battery, 0, 1, 2)
        pixels                : Node = Node('pixels', battery, 0, 1, 2500)
        quantum_processor     : Node = Node('quantum processor', battery, 0, 1, 1)
        silicon_board         : Node = Node('silicon board', quantum_processor, 0, 1, 4)
        protocite_bar2        : Node = Node('protocite bar', silicon_board, 0, 1, 2)
        thorium_rod           : Node = Node('thorium rod', battery, 0, 1, 5)
        thorium_ore           : Node = Node('thorium ore', thorium_rod, 0, 1, 2)
        reversearithmetic(industrial_battery, random.randint(1, 10))
        if not os.path.exists(TESTFILENAME):
            # create the file
            pandas.DataFrame(columns=FIELDNAMES).to_csv(TESTFILENAME, index=False)
            self.test_pandascsvwrite()  # call the function again to write to the file
        else:
            # write preset mock ingredient tree onto it
            for line in industrial_battery.create_csv_writerows([]):
                pandas.DataFrame(line, index=[0]).to_csv(TESTFILENAME, mode='a', header=False, index=False)
        # TODO: implement your test here
        # self.skipTest(exep_msg.testnotadded())
        # test that the file exists
        self.assertTrue(os.path.exists(TESTFILENAME))

    def test_pandascsvread(self):
        """
        if file does not exist, raise an error
        if the file already exists, open it in read mode and read the data
        """
        if not os.path.exists(TESTFILENAME):
            #!            raise FileNotFoundError(exep_msg.csvnotexist())
            self.skipTest(exep_msg.csvnotexist())  # skip the test
        # TODO: implement your test here
        else:
            # value is the treekey and the item is the headnode translated from the csv file
            foundheadpoints: dict = {}
            # turn a row of the csv data into a dictionary
            mypyandas = pandas.read_csv(TESTFILENAME)  # read the csv file
            rowDict2 : dict = pandas.read_csv(TESTFILENAME).to_dict('index')
            # @audit-info convert row into a list, use a boolean to detect if the nesscary values are present in the proper positions of the list to match a head node of the tree, and if it does input it the dictionary of head nodes
            # @audit-info headinstance condition is met if list[index=3] is None,list[index=4] is 0, list[index=5] = 1, and list[index=6] = 1
            for purple in pandas.read_csv(TESTFILENAME).to_dict('index').items():  # iterate through the rows of the dataframe
                blue = purple[1].values()
                green : list = list(purple[1].values())  # convert the values of the dictionary to a list
                # @note conversion syntax: yellow : Node = Node(green[1],None,green[4],green[5],green[6])  # create a node from the list
                isheadinstance : bool = green[3] is None and green[4] == 0 and green[5] == 1 and green[6] == 1  # check if the node is a head node
                if isheadinstance:  # add the head node to the dictionary of head nodes
                    foundheadpoints.update({green[0]: Node(green[1], None, green[4], green[5], green[6])})  
            self.assertGreaterEqual(len(foundheadpoints), 1, 'No headnodes found')  # assert that the headnodes are found

            
    def test_findheadnodes(self):
        """
        test parsing the csv file to find head node instances
        """
        # TODO: implement your test here
        self.skipTest(exep_msg.testnotadded())


if __name__ == '__main__':
    unittest.main()
