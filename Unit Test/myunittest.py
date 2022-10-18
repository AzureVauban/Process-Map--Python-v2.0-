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

    def test_rowoutput(self):
        """
        test if the row output is correct
        """
        parent_ingredient: str = 'None'
        if self.coal.parent is not None:
            parent_ingredient = self.coal.parent.ingredient
        testlist: list = [
            self.coal.ingredient,
            parent_ingredient,
            str(self.coal.amountonhand*0),
            str(self.coal.amountmadepercraft),
            str(self.coal.amountneeded),
            str(self.coal.generation),
            self.coal.treekey
        ]
        assertlist: list = self.coal.create_csv_string()  # pylint: disable=no-member
        self.assertListEqual(testlist, assertlist, 'The list is not equal')
    # create a mock csv file and test the write to it

    def test_existance(self):
        """test if the file exists in the current directory"""
        # test if the file exist in the current directory
        self.assertTrue(os.path.isfile(filename))


        """create a mock csv file"""
        # test if the file exists in the current folder of the directory
        fieldnames = [  # comments are examples of the header
            'Ingredient',  # Coal
            'Parent of Ingredient',  # Carbon
            'Amount on Hand',  # 0
            'Amount Made Per Craft',  # 1
            'Amount Needed Per Craft',  # 10
            'Generation',  # 1
            'Tree Key\n'  # 74nry8keki
        ]
        ispresentindirectory: bool = os.path.isfile(filename)
        # if the file is not in the current directory create it
        if not ispresentindirectory:
            # if the file is not in the current directory create it with 'UTF-8' encoding
            with open(filename, 'w', encoding='UTF-8', newline='') as csvfile:
                # write the header
                # write the header onto the csv file
                csvfile.write(','.join(fieldnames))
                self.carbon.writecsvoutput(filename)  # pylint: disable=no-member
        else:  # if the csv file is already in the current directory, just write to it
            # write the header onto the csv file
            with open(filename, 'w', encoding='UTF-8', newline='') as csvfile:
                csvfile.write(','.join(fieldnames))
                tentativevar_red : list = self.carbon.create_tree_csv([])
        for olive_colored_node in olivegreen.children.items():
            self.test_createmockfile(olive_colored_node[1])
        self.assertTrue(os.path.isfile(filename))

    def test_writetoCSV(self, cherryred=carbon):
        """_summary_
        """
        # write header
        with open(filename, 'w', encoding='UTF-8', newline='') as csvfile:
            # itterate through the tree and write to csv
            csvfile.write(','.join(cherryred.create_csv_string()))  # pylint: disable=no-member
            csvfile.close()
            for childnode in cherryred.children.items():
                self.test_writetoCSV(childnode[1])
        # check if the csv file is created
        self.assertTrue(os.path.isfile(filename))
