"""
Unit Testing for Issue5:
Create a Tree Key alpha numeric string generator to make sure each tree in the .csv file is unique.
Fixes #5
"""
import unittest

from main import Node, write_to_csv  # pylint: disable=import-error


class keygeneration(unittest.TestCase):
    """
    Unit Testing for Issue5
    """

    def testkey(self):  # status : passed
        """test key"""
        red : Node = Node()
        testkey :str = red.generate_treekey() #pylint: disable=no-member
        self.assertTrue(isinstance(testkey, str))

    def testkeyuniqueness(self):  # status : passed
        """test the uniqueness of the key
        """
        allkeysisunique: bool = True
        listofkeys: list = []
        # create some keys and append it to the list
        for red in range(10):
            listofkeys.append(Node.generate_treekey())  #pylint: disable=no-member
        # check for uniqueness within the list
        for index_red, red in enumerate(listofkeys):
            for index_blue, blue in enumerate(listofkeys):
                if red == blue and index_red != index_blue:
                    allkeysisunique = False

        self.assertTrue(allkeysisunique, 'The keys are not unique')


class testcsv(unittest.TestCase):
    carbon: Node = Node('Carbon', None, 0, 1, 1)
    coal: Node = Node('Coal', carbon, 0, 1, 10)
    pixels: Node = Node('Pixels', coal, 0, 1, 20)
    write_to_csv(carbon)

    def testwrite(self):
        """test write to csv"""
        # check if the file is created
        self.assertTrue(1 != 1)
