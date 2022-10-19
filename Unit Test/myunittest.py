"""
Unit Testing for Issue5:
Create a Tree Key alpha numeric string generator to make sure each tree in the .csv file is unique.
Fixes #5
"""
import csv
from gzip import _OpenTextMode
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

    def testcsvlinedict(self):
        """test the csv line dict creation method"""
        mi_go: dict = self.carbon.create_csv_rows({})
        self.assertTrue(isinstance(mi_go, dict))

    def test_existance(self):
        """test if the file exists in the current directory"""
        ispresentindirectory: bool = os.path.isfile(filename)
        # test if the file exists in the current folder of the directory
        fieldnames = [  # pylint: disable=unused-variable
            'Tree_Key',  # 74nry8keki
            'Ingredient',  # Coal
            'Parent_of_Ingredient',  # Carbon
            'Amount_on_Hand',  # 0
            'Amount Made Per Craft',  # 1
            'Amount Needed Per Craft',  # 10
            'Generation'  # 1
        ]
        rows: list = [  # pylint: disable=unused-variable
            {'Tree Key': '# 74nry8keki',
             'Ingredient': 'Coal',
             'Parent_of_Ingredient': 'Carbon',
             'Amount_on_Hand': '0',
             'Amount_Made_Per_Craft': '1',
             'Amount_Needed_Per_Craft': '10',
             'Generation': '1'
             }
        ]
        if ispresentindirectory:  # file already exists, write data to it
            pass
        else:  # file does not exist, create it and write data to it
            #open file in write mode with UTF8 encoding
            with open(filename, 'w', encoding='UTF8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                #write header
                writer.writeheader()
#!                writer.writerows(rows)
                #write rows using writedict method  
                nyarlathotep: list = self.carbon.create_csv_rows({})
                writer.writerows(nyarlathotep)
        # check if the file is present in the current directory
        self.assertTrue(os.path.isfile(filename))
