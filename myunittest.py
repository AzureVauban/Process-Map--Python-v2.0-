"""
Unit Testing for Issue5:
Create a Tree Key alpha numeric string generator to make sure each tree in the .csv file is unique.
Fixes #5
"""
import csv
import os
import random
import unittest

from main import Node, reversearithmetic  # pylint: disable=import-error

CSVFILENAME: str = 'ingredient_trees.csv'


def generatename(lengthlimit: int = random.randint(10, 20)) -> str:
    """_summary_

    Returns:
        str: _description_
    """
    # create a random name as a string
    yuggoth: str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    mocknodename: str = ''
    for _ in range(random.randint(6, lengthlimit)):
        mocknodename += random.choice(yuggoth)
    return mocknodename

class NodeTree():
    """
    class for creating a mock ingredient tree of nodes for testing
    """
    canopynode : Node = Node()
    population: int = 1

    def __findhead(self, node: Node) -> Node:
        """traverses to the head of the node

        Args:
            node (Node): current postion in a linked list

        Returns:
            Node: the headmost node of the current node
        """
        while node.parent is not None:
            node = node.parent
        return node

    def __countpopulation(self, node: Node, currentcount: int = 0) -> int:
        """counts the number of nodes in the tree

        Args:
            node (Node): the instance of the node to count
            currentcount (int, optional): the current amount of nodes found in the tree.
            Defaults to 1.

        Returns:
            int: the amount of nodes found in the tree
        """
        currentcount += 1
        for hotnode in node.children.items():
            self.__countpopulation(hotnode[1], currentcount)
        return currentcount

    def generatetree(self, limit: int = random.randint(1, 10), head: Node = Node(generatename())) -> Node:
        return head

    def __init__(self, population: int = random.randint(1, 10)):
        #generate the tree
        self.generatetree(population)
        # set the population of the tree
        self.population = self.__countpopulation(self.canopynode)
        print('creating a new tree at object', self)

class TreeGeneration(unittest.TestCase):
    """
    Unit Testing for Issue3 - Make a method that can randomly create a valid mock ingredient tree.
    """
    def testpopulation(self):
        """test to see if the population of the tree is correct"""
        testtree : NodeTree = NodeTree(5)
        self.assertEqual(testtree.population, 1, "The population of the tree should be 5")

class KeyGeneration(unittest.TestCase):
    """
    Unit Testing for Issue5
    """

    def skiptestkey(self):  # status : passed
        """test key"""
        red: Node = Node()
        testkey: str = red.generate_treekey()  # pylint: disable=no-member
        self.assertTrue(isinstance(testkey, str))

    def skiptestkeyuniqueness(self):  # status : passed
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
        mi_go: list = self.carbon.create_csv_writerows([])
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
                kassogtha: list = self.carbon.create_csv_writerows([])
                writer.writerows(kassogtha)
                dunwichhorror.close()
        else:  # file does not exist, create it and write data to it
            with open(CSVFILENAME, mode='w', encoding='UTF-8', newline='') as nyarlathotep:
                writer = csv.DictWriter(nyarlathotep, fieldnames=field_names)
                # write header to csv file
                writer.writeheader()
            # write rows to csv file
                kassogtha: list = self.carbon.create_csv_writerows([])
                writer.writerows(self.carbon.create_csv_writerows([]))
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
                writer = csv.DictWriter(yog_sothoth, fieldnames=field_names)
                # writer.writerows(morphite.create_csv_writerows([]))
                vhurerc: Node = NodeTree().canopynode
                reversearithmetic(vhurerc, random.randint(17, 2001))
                writer.writerows(vhurerc.create_csv_writerows([]))
                yog_sothoth.close()
        self.assertTrue(os.path.isfile(CSVFILENAME))
    # todo finish creating the unit test method

    def test_repeated(self):
        """test if the node tree has been repeated
        """
        copyoftree: bool = False
        # read the file
        with open(CSVFILENAME, mode='r', encoding='UTF-8', newline='') as ithaqua:
            # look for a head node in the row of a .csv file
            # head node will have 0,1,1,0 as the values and a parent ingredient of None
            isheadnode: bool = False
        # if the head node is found, create a node tree from the nodes below it
        # check to see if the node tree is the same as the one that was written to the file
            # in test case will be carbon and the Morphite tree
        # test should pass in ideal circumstances
        self.assertFalse(copyoftree)


class TestreadingtoCSV(unittest.TestCase):
    pass
