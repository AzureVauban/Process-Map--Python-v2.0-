"""
Unit Testing for Issue5:
Create a Tree Key alpha numeric string generator to make sure each tree in the .csv file is unique.
Fixes #5
"""
import csv
import os
import unittest

from main import Node  # pylint: disable=import-error


filename: str = 'ingredient_trees.csv'


class keygeneration(unittest.TestCase):
    """
    Unit Testing for Issue5
    """

    def testkey(self):  # status : passed
        """test key"""
        red: Node = Node()
        testkey: str = red.generate_treekey()  # pylint: disable=no-member
        self.assertTrue(isinstance(testkey, str))

    def testkeyuniqueness(self):  # status : passed
        """test the uniqueness of the key
        """
        allkeysisunique: bool = True
        listofkeys: list = []
        # create some keys and append it to the list
        for red in range(10):
            listofkeys.append(Node.generate_treekey()
                              )  # pylint: disable=no-member
        # check for uniqueness within the list
        for index_red, red in enumerate(listofkeys):
            for index_blue, blue in enumerate(listofkeys):
                if red == blue and index_red != index_blue:
                    allkeysisunique = False

        self.assertTrue(allkeysisunique, 'The keys are not unique')


class TestCSV(unittest.TestCase):
    """
    create a mock csv file and test the write_to_csv
    """
    # mock ingredient tree for carbon csv file
    carbon: Node = Node('Carbon', None, 0, 1, 1)
    coal: Node = Node('Coal', carbon, 0, 1, 10)
    pixels: Node = Node('Pixels', coal, 0, 1, 20)

    # create a mock csv file and test the write to it
    def test_existance(self):
        """test if the file exists in the current directory"""
        # test if the file exist in the current directory
        self.assertTrue(os.path.isfile(filename))

    def test_createmockfile(self):
        """create a mock csv file"""
        # test if the file exists in the current folder of the directory
        ispresentindirectory: bool = os.path.isfile(filename)
        # if the file is not in the current directory create it
        if not ispresentindirectory:
            # if the file is not in the current directory create it with 'UTF-8' encoding
            with open(filename, 'w', encoding='UTF-8', newline='') as csvfile:
                # write the header
                fieldnames = [  # comments are examples of the header
                    'Ingredient',  # Coal
                    'Parent of Ingredient',  # Carbon
                    'Amount on Hand',  # 0
                    'Amount Made Per Craft',  # 1
                    'Amount Needed Per Craft',  # 10
                    'Generation',  # 1
                    'Tree Key'  # 74nry8keki
                ]
                # write the header onto the csv file

        self.assertTrue(os.path.isfile(filename))

    def test_writetoCSV(self):
        # write header
        # itterate through the tree and write to csv
        # check if the csv file is created
        pass
