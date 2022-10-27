"""
Unit Testing for Issue5:
Create a Tree Key alpha numeric string generator to make sure each tree in the .csv file is unique.
Fixes #5 (temporarily pause working on this issue to work on the searching/clone methods)
"""
import csv
import os
import unittest

from main import Node  # pylint: disable=import-error

CSVFILENAME: str = 'ingredient_trees.csv'



class TreeGeneration(unittest.TestCase):
    """
    Unit Testing for Issue3 - Make a method that can randomly create a valid mock ingredient tree.
    """
    def testpopulation(self):
        """test to see if the population of the tree is correct"""
        unittest.SkipTest('NodeTree class needs debugging')



field_names = [
    'Tree_Key',  # 74nry8keki
    'Ingredient',  # Coal
    'Parent_of_Ingredient',  # Carbon
    'Amount_on_Hand',  # 0
    'Amount_Made_Per_Craft',  # 1
    'Amount_Needed_Per_Craft',  # 10
    'Generation'  # 1
]

class TestwritingtoCSV(unittest.TestCase):
    """
    create a mock csv file and test the write_to_csv
    """
    # mock ingredient tree for carbon csv file
    carbon: Node = Node('Carbon', None, 0, 1, 1)
    coal: Node = Node('Coal', carbon, 0, 1, 10)
    pixels: Node = Node('Pixels', coal, 0, 1, 20)
    fileexistsalready: bool = os.path.isfile(CSVFILENAME)

    def testcsvlinedict(self):
        """test the csv line dict creation method"""
        mi_go: list = self.carbon.create_csv_writerows([]) #pylint:disable=no-member
        self.assertTrue(isinstance(mi_go, list))

    def test_existance(self):
        """test if the file exists in the current directory
        """
        ispresentindirectory: bool = os.path.isfile(CSVFILENAME)
        # test if the file exists in the current folder of the directory
        rows: list = [  # pylint: disable=unused-variable
            { 
                'Tree Key': '# 74nry8keki', 
                'Ingredient': 'Coal',
                'Parent_of_Ingredient': 'Carbon',
                'Amount_on_Hand': '0',
                'Amount_Made_Per_Craft': '1',
                'Amount_Needed_Per_Craft': '10',
                'Generation': '1'
            }
        ]
        if ispresentindirectory:  # file already exists, write data to it
            with open(CSVFILENAME, mode='w', encoding='UTF-8', newline='') as dunwichhorror:
                writer = csv.DictWriter(dunwichhorror, fieldnames=field_names)
                writer.writeheader()
                kassogtha: list = self.carbon.create_csv_writerows([])#pylint:disable=no-member
                writer.writerows(kassogtha)
                dunwichhorror.close()
        else:  # file does not exist, create it and write data to it
            with open(CSVFILENAME, mode='w', encoding='UTF-8', newline='') as nyarlathotep:
                writer = csv.DictWriter(nyarlathotep, fieldnames=field_names)
                # write header to csv file
                writer.writeheader()
            # write rows to csv file
                kassogtha: list = self.carbon.create_csv_writerows([])#pylint:disable=no-member
                writer.writerows(self.carbon.create_csv_writerows([]))#pylint:disable=no-member
                # close csv file
                nyarlathotep.close()
        self.assertTrue(os.path.isfile(CSVFILENAME))

    def test_append(self):
        """test appending to the csv file when the file already exists
        """
        if not self.fileexistsalready:
            raise ValueError(
                'The file does not exist in your current directory')
        else:
            morphite: Node = Node('Morphite', None, 0, 1,1)  # pylint: disable=invalid-name
            irradiumbar: Node = Node('Irradium Bar', morphite, 0, 1, 1)  # pylint: disable=invalid-name
            irradiumore: Node = Node('Irradium Ore', irradiumbar, 0, 1, 2)  # pylint: disable=invalid-name
            pixels: Node = Node('Pixels', irradiumore, 0, 1,600)  # pylint: disable=unused-variable
            liquidprotocite: Node = Node('Liquid Protocite', morphite, 0, 1, 1)  # pylint: disable=invalid-name
            liquidprotociteb: Node = Node('Liquid Protocite B', liquidprotocite, 0, 2, 1)  # pylint: disable=unused-variable
            pus: Node = Node('Pus', liquidprotocite, 0, 2,1)  # pylint: disable=invalid-name
            blistersack: Node = Node('Blister Sack', pus, 0, 1, 1)  # pylint: disable=unused-variable
            phasematter: Node = Node('Phase Matter', morphite, 0, 1, 1)  # pylint: disable=invalid-name
            pixelsb: Node = Node('Pixels B', phasematter,0, 1, 150)  # pylint: disable=unused-variable
            sulphuricacid: Node = Node('Sulphuric Acid', morphite, 0, 1, 2)  # pylint: disable=invalid-name
            whitespine: Node = Node('Whitespine', sulphuricacid, 0, 2, 1)  # pylint: disable=unused-variable
            # append this fake tree onto the file, not OVERWRITE it
            with open(CSVFILENAME, mode='a', encoding='UTF-8', newline='') as yog_sothoth:  # pylint: disable=invalid-name
                # ? to append to the file, open in it mode='a'
                writer = csv.DictWriter(yog_sothoth, fieldnames=field_names) #pylint:disable=unused-variable
                # writer.writerows(morphite.create_csv_writerows([]))
                #!!vhurerc: Node = NodeTree().canopynode
                #!!reversearithmetic(vhurerc, random.randint(17, 2001))
                #!!writer.writerows(vhurerc.create_csv_writerows([]))
                #!!yog_sothoth.close()
        #!!self.assertTrue(os.path.isfile(CSVFILENAME))
        unittest.SkipTest('skipping test_append, reworking of the NodeTree class is needed')

    def test_repeated(self):
        """test if the node tree has been repeated
        """
        copyoftree: bool = False #pylint:disable=unused-variable
        # read the file
        with open(CSVFILENAME, mode='r', encoding='UTF-8', newline='') as ithaqua: #pylint:disable=unused-variable
            # look for a head node in the row of a .csv file
            # head node will have 0,1,1,0 as the values and a parent ingredient of None
            isheadnode: bool = False #pylint:disable=unused-variable
        # if the head node is found, create a node tree from the nodes below it
        # check to see if the node tree is the same as the one that was written to the file
            # in test case will be carbon and the Morphite tree
        # test should pass in ideal circumstances
        #!!self.assertFalse(copyoftree)
        unittest.SkipTest('skipping test_repeated, reworking of the NodeTree class is needed in order to implement this test')


class TestreadingtoCSV(unittest.TestCase):
    """tentative_description_

    Args:
        unittest (_type_): tentative_description_
    """
    def tentativetest(self):
        """tentative_description
        """
        unittest.SkipTest('skipping test_repeated, reworking of the NodeTree class is needed in order to implement this test, implementation of methods to reading the csv file is needed')
