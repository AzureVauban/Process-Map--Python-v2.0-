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

class tentative_class_name():  
    """_summary_
    """
    tentative_name_nodeobject: Node  
    # return the number of nodes generated in the tree
    tentative_name_intobject: int = 1
    def __verifyuniqueness(self, tentativename_stringobject: str, tentativename_nodeobject2: Node) -> bool:
        """_summary_

        Returns:
            bool: _description_
        """
        # verify that the string generated is unique
        if tentativename_stringobject == tentativename_nodeobject2.ingredient:
            return False
        else:
            for childnode in self.tentative_name_nodeobject.children.items():
                self.__verifyuniqueness(tentativename_stringobject, childnode[1])
        return True

    def createtree(self,treepopulationlimit: int = random.randint(2, 50), headnode: Node = Node(generatename(), None)) -> Node:
        """
        creates a randomly generated ingredient tree
        """
        childrenpopulation: int = treepopulationlimit-1
        for _ in range(childrenpopulation):
            generated_random_name: str = generatename()
            while not self.__verifyuniqueness(generated_random_name, headnode):
                generated_random_name: str = generatename()
                self.__verifyuniqueness(generated_random_name, headnode)
            Node(generatename(), headnode, 0,
                random.randint(1, 1000), random.randint(1, 1000))
            self.tentative_name_intobject += 1
            if self.tentative_name_intobject > treepopulationlimit:
                return headnode
        for child in headnode.children.items():
            self.createtree(treepopulationlimit-1, child[1])
        return headnode

    def returningredients(self,nodeobject: Node, storednames: list) -> list:
        storednames.append(nodeobject.ingredient)
        for child in nodeobject.children.items():
            self.returningredients(child[1], storednames)
        return storednames

    def returngenerationleafletscount(self,startingnode : Node,depth: int = 1,cur_counter : int = 0) -> int:
        """_summary_

        Args:
            depth (int, optional): _description_. Defaults to 1.

        Returns:
            int: _description_
        """
        # returns the number of all the nodes at a given depth in the tree
        if startingnode.generation == depth:
            cur_counter+=1
        return cur_counter

    def __init__(self, max_population_size: int =random.randint(5,50)) -> None:
        self.tentative_name_head = self.createtree(max_population_size)



class TreeGeneration(unittest.TestCase):
    """
    Unit Testing for Issue3 - Make a method that can randomly create a valid mock ingredient tree.
    """

    def test_generate_randomstring(self):
        """
        test to see if the random string generator is working
        """
        assertstrings: list = []
        for _ in range(1000):
            assertstrings.append(generate_randomstring())
        for string in assertstrings:

            self.assertGreaterEqual(len(string), 6)

    def test_generate_tree_population(self):
        """test that the size of the generated tree is equal to or greater than the population limit augment passed into the method

        Raises:
            ValueError: duplicate ingredient name on the same index has been found
        """
        populationsize: int = random.randint(2, 50)
        testnodetree: Node = generate_tree(treepopulationlimit=populationsize)
        debug_listofingredients: list = recursive_treeparse_listnames(
            testnodetree, [])  # pylint: disable=unused-variable
        asserttreesize: int = count_population(testnodetree, 0)
        for redindex, red in enumerate(debug_listofingredients):
            for blueindex, blue in enumerate(debug_listofingredients):
                if red == blue and blueindex != redindex:
                    raise ValueError(
                        'duplicate ingredient name on the same index has been found')
        self.assertGreaterEqual(asserttreesize, populationsize)


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
            morphite: Node = Node('Morphite', None, 0, 1,
                                  1)  # pylint: disable=invalid-name
            irradiumbar: Node = Node(
                'Irradium Bar', morphite, 0, 1, 1)  # pylint: disable=invalid-name
            irradiumore: Node = Node(
                'Irradium Ore', irradiumbar, 0, 1, 2)  # pylint: disable=invalid-name
            pixels: Node = Node('Pixels', irradiumore, 0, 1,
                                600)  # pylint: disable=unused-variable
            liquidprotocite: Node = Node(
                'Liquid Protocite', morphite, 0, 1, 1)  # pylint: disable=invalid-name
            liquidprotociteb: Node = Node(
                'Liquid Protocite B', liquidprotocite, 0, 2, 1)  # pylint: disable=unused-variable
            pus: Node = Node('Pus', liquidprotocite, 0, 2,
                             1)  # pylint: disable=invalid-name
            blistersack: Node = Node(
                'Blister Sack', pus, 0, 1, 1)  # pylint: disable=unused-variable
            phasematter: Node = Node(
                'Phase Matter', morphite, 0, 1, 1)  # pylint: disable=invalid-name
            pixelsb: Node = Node('Pixels B', phasematter,
                                 0, 1, 150)  # pylint: disable=unused-variable
            sulphuricacid: Node = Node(
                'Sulphuric Acid', morphite, 0, 1, 2)  # pylint: disable=invalid-name
            whitespine: Node = Node(
                'Whitespine', sulphuricacid, 0, 2, 1)  # pylint: disable=unused-variable
            # append this fake tree onto the file, not OVERWRITE it
            with open(CSVFILENAME, mode='a', encoding='UTF-8', newline='') as yog_sothoth:  # pylint: disable=invalid-name
                # ? to append to the file, open in it mode='a'
                writer = csv.DictWriter(yog_sothoth, fieldnames=field_names)
                # writer.writerows(morphite.create_csv_writerows([]))
                vhurerc: Node = generate_tree()
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
