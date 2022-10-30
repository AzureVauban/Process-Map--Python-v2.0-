"""
Unit Tests for the solution.py module
- outputting data to a .csv file for later use
- inputting data to a .csv file for utilization
- search for a node in the tree and copy it instead of retyping all your data
- inputting basic arithmetic symbols when prompted to input numeric data (not added yet)
"""
import os
import unittest
import random
import pandas
from solution import Node, generatename, createclone, reversearithmetic
FIELDNAMES: list = [  # list of field names for the csv output file (new csv file)
    'Tree_Key',  # 74nry8keki',
    'Ingredient',  # Copper Wire
    'Ingredient_Alias',  # Copper_Wire__ZpgMzAwQdfRu
    'Parent_of_Ingredient',  # Silicon Board
    'Amount_on_Hand',  # 0
    'Amount_Of_Parent_Made_Per_Craft',  # 9
    'Amount_Needed_Per_Craft',  # 0
    'Generation'  # 1
]
TESTFILENAME: str = "tests_solution.csv"


class NodeCreationTests(unittest.TestCase):

    def testcheckclone(self):
        """
        test that the clone is created correctly
        """
        tomato: Node = Node('tomato')
        tomahto = createclone(tomato)
        self.assertIsNot(tomato, tomahto, 'Clone is not at a unique location')


class internalsearch(unittest.TestCase):
    # test ingredient tree
    industrial_battery: Node = Node(
        'industrial battery', None, treekey=Node.generate_treekey())
    protocite_bar: Node = Node('protocite bar', industrial_battery, 0, 1, 5)
    protocite: Node = Node('protocite', protocite_bar, 0, 1, 2)
    battery: Node = Node('battery', industrial_battery, 0, 1, 2)
    pixels: Node = Node('pixels', battery, 0, 1, 2500)
    quantum_processor: Node = Node(
        'quantum processor', industrial_battery, 0, 1, 1)
    silicon_board: Node = Node('silicon board', quantum_processor, 0, 1, 4)
    protocite_bar2: Node = Node('protocite bar', quantum_processor, 0, 1, 2)
    protocite2: Node = Node('protocite', protocite_bar2, 0, 1, 2)
    thorium_rod: Node = Node('thorium rod', industrial_battery, 0, 1, 5)
    thorium_ore: Node = Node('thorium ore', thorium_rod, 0, 1, 2)

    def search(self, ingredient: str, node: Node, foundnodes: dict) -> dict:
        """
        return a dictionary of nodes that have the same name as the ingredient
        """
        if node is None:
            raise ValueError('Node is None')
        if node.ingredient == ingredient and node.parent is not None:
            foundnodes.update({node.instancekey: node})
        for child in node.children.items():
            self.search(ingredient, child[1], foundnodes)
        if len(foundnodes) == 0:
            return {-1: None}
        else:
            return foundnodes

    def search2(self, ingredient: str, head: Node) -> dict:
        # create a dict of all the nodes that have the same ingredient name
        # the dict should have a key of the instancekey and a value of the node
        returndict: dict = {}
        # search for node
        for node in self.converttreeintodict(head, {}).items():
            if node[1].ingredient == ingredient:
                returndict.update({node[1].instancekey: node[1]})
        # if the length of the dict is 0, return {-1:None} else return the dict
        if len(returndict) == 0:
            return {-1: None}
        else:
            return returndict

    def converttreeintodict(self, head: Node, nodes: dict) -> dict:
        nodes.update({head.instancekey: head})
        for child in head.children.items():
            self.converttreeintodict(child[1], nodes)
        return nodes

    def test_createclone(self):
        # assert that the clone node is not the same memory address as the original node
        searchdict: dict = self.search2('protocite', self.industrial_battery)

    def test_search(self):
        # assert that the search method does not return {-1:None}
        testsearchstring: str = 'protocite'
        assertDict: dict = self.search(
            testsearchstring, self.industrial_battery, {})
        if len(assertDict) == 1:
            print('We noticed that you typed in', testsearchstring, len(
                assertDict), 'time already, do you want to copy the contents of that node?')
        else:
            print('We noticed that you typed in', testsearchstring, len(
                assertDict), 'times already, do you want to copy the contents of that node?')
        self.assertNotEqual(assertDict, {-1: None}, 'No nodes found')


class CSVsutilization(unittest.TestCase):
    """
    @note use pandas instead of built in csv module

    Args:
        unittest (_type_): _description_
    """
    # @audit-info use df.iloc to read an entire row of data
    # @audit-info use df.columns to read the column names
    # @audit-info use df.iterrows to iterate through the rows of the dataframe (dataframe referred to as df and the csvfile)

    # @note mock ingredient tree for industral battery https://frackinuniverse.miraheze.org/wiki/Industrial_Battery
    @classmethod
    def countpopulation(cls, node: Node, count: int = 0) -> int:
        """
        count how many subnodes are connected parameter node
        @audit-info use a recursive function to count the population of the tree, start off with the head node!
        Args:
            node (Node): node to count the subnodes of
            count (int, optional): integer number of counted nodes. Defaults to 0.

        Returns:
            int: population of the node's tree
        """
        count += 1
        if len(node.children.items()) > 0:
            for child in node.children.items():
                count = cls.countpopulation(child[1], count)
        return count
    industrial_battery: Node = Node('industrial battery', None, treekey=Node.generate_treekey())
    protocite_bar: Node = Node('protocite bar', industrial_battery, 0, 1, 5)
    protocite: Node = Node('protocite', protocite_bar, 0, 1, 2)
    battery: Node = Node('battery', industrial_battery, 0, 1, 2)
    pixels: Node = Node('pixels', battery, 0, 1, 2500)
    quantum_processor: Node = Node('quantum processor', industrial_battery, 0, 1, 1)
    silicon_board: Node = Node('silicon board', quantum_processor, 0, 1, 4)
    protocite_bar2: Node = Node('protocite bar', quantum_processor, 0, 1, 2)
    thorium_rod: Node = Node('thorium rod', industrial_battery, 0, 1, 5)
    thorium_ore: Node = Node('thorium ore', thorium_rod, 0, 1, 2)
    reversearithmetic(industrial_battery, random.randint(1, 10))

    # todo finish creating this class and utilize it in reading and writing tests (not using a preset tree)
    class RandomNodeTree:
        population: int = 0
        head: Node

        def generateTree(self, popuation: int = random.randint(1, 10), monokai: Node = Node(generatename())) -> Node:
            # the population of the tree cannot suprass the population parameter
            # do not continue the method if the count of the tree from head node is equal to or greater than the population parameter
            if CSVsutilization.countpopulation(monokai) >= popuation:
                # generate a random number between 1 and 10 and reverse the arithmetic of the head node
                return monokai
            else:
                return monokai

        def __init__(self, population: int = random.randint(1, 10), head: Node = Node(generatename())) -> None:
            self.head = head

    def testsubstringmethod(self,):
        # reformat a string to have all of its whitespace turn into an underscore
        teststring: str = 'this is a test string'  # test string
        teststring = teststring.strip()
        # replace all whitespace with underscores
        teststring = teststring.replace(' ', '_')
#!        self.assertEqual(teststring, 'this_is_a_test_string')  # assert that the string is formatted correctly
        self.skipTest('Test is not needed anymore')  # skip the test

    def test_pandascsvwrite(self, yellowduck: Node = industrial_battery):
        """
        if file does not exist in the SAME directory as the solution module, create it and write to it
        if the file already exists, open it in append mode and append written data to it
        """
        # prepared mock ingredient append data

        if not os.path.exists(TESTFILENAME):
            # create the file
            pandas.DataFrame(columns=FIELDNAMES).to_csv(
                TESTFILENAME, index=False)
            self.test_pandascsvwrite()  # call the function again to write to the file
            self.skipTest('csv file does not exist')  # skip the test
        else:
            # write preset mock ingredient tree onto it
            for line in yellowduck.create_csv_writerows([]):
                pandas.DataFrame(line, index=[0]).to_csv(
                    TESTFILENAME, mode='a', header=False, index=False)
        # test that the file exists
        self.assertTrue(os.path.exists(TESTFILENAME))

    # todo turn this into a function in the solution module when this unit test passes
    def test_pandacsvparsesearch(self,filename : str = TESTFILENAME) -> dict:
        """
        test parsing the csv file to find head node instances

        if file does not exist, skip the test (in the solution module return {-1:None} instead)
        if the file already exists, open it in read mode
            parse the csv file to see if there are any rows of data that match the 
            conditions of a head node instance, if they do create a head node instance and add it into a returnable dict
        """
        if not os.path.exists(TESTFILENAME):
            self.skipTest('csv file does nto exist')  # skip the test
            # return a dict with a key of -1 and a value of None
            return {-1: None}
        else:
            # value is the treekey and the item is the headnode translated from the csv file
            foundheadpoints: dict = {}
            # turn a row of the csv data into a dictionary
            # @audit-info convert row into a list, use a boolean to detect if the nesscary values are present in the proper positions of the list to match a head node of the tree, and if it does input it the dictionary of head nodes
            # @audit-info headinstance condition is met if list[index=3] is None, list[index=5] = 1, list[index=6] = 1, adn list[index=7] = 0
            # iterate through the rows of the dataframe
            for purple in pandas.read_csv(TESTFILENAME).to_dict('index').items():
                # convert the values of the dictionary to a list
                green: list = list(purple[1].values())
                # todo format ingredient alias to match the ingredient (rowlist[3] == rowlist[1])

                # @note conversion syntax: yellow : Node = Node(green[1],None,green[5],green[6],green[6])  # create a node from the list
                # @note isheadinstance: bool = green[3] == 'None' and green[5] == 1 and green[6] == 1 and green[7] == 0
                # if the conditions are met for it to mock a head node
                if green[3] == 'None' and green[5] == 1 and green[6] == 1 and green[7] == 0:
                    # create a node from the row's data
                    # add the node to the dictionary of head nodes
                    foundheadpoints.update({green[0]: Node(
                        green[1], None, green[4], green[5], green[6], False, False, green[0])})
                # @note when this is turned into a function, if the returned dictionary is empty, return {-1:None} instead of an empty dictionary
            # check that the key of the dictionary and the treekey of the node are the same, if they are not, raise an exception
            for key, value in foundheadpoints.items():
                if key != value.treekey:
                    # raise an exception
                    raise ValueError(
                        'the key of the dictionary and the treekey of the node are not the same')
            # assert that the headnodes are found
            self.assertGreaterEqual(
                len(foundheadpoints), 1, 'No headnodes found')
            return foundheadpoints  # return the headnodes

    def emplacelink(self, parent: Node, csvrow: list) -> bool:
        """
        @audit when this method is called, it should be called when the node is going through the tree recursively and the csvrow being constant throughout that recursive search
        @audit-info return a boolean value to indicate if the node was successfully linked to the parent node
        csvrow : [
            @note example row for a head node instance
            'Tree_Key'                          [0]: 'cE1NXAKBXatn'
            'Ingredient'                        [1]: 'industrial battery'
            'Ingredient_Alias'                  [2]: 'industrial_battery'
            'Parent_of_Ingredient'              [3]: 'None'
            'Amount_on_Hand'                    [4]: 7 #? can be any integer value
            'Amount_Of_Parent_Made_Per_Craft'   [5]: 1
            'Amount_Needed_Per_Craft'           [6]: 1
            'Generation'                        [7]: 0
        ]
        csvrow : [
            @note example row for a child instance
            'Tree_Key'                          [0]: 'cE1NXAKBXatn'
            'Ingredient'                        [1]: 'protocite bar'
            'Ingredient_Alias'                  [2]: 'protocite_bar__RQ1skwPB7PsdymWjQ' @note __RQ1skwPB7PsdymWjQ could be formatted out of the string
            #? will have something like '__RQ1skwPB7PsdymWjQ' if there is a repeat of that ingredient name in the tree
            'Parent_of_Ingredient'              [3]: 'industrial battery' #? must not be 'None'
            'Amount_on_Hand'                    [4]: 35 #? can be any integer value
            'Amount_Of_Parent_Made_Per_Craft'   [5]: 1
            'Amount_Needed_Per_Craft'           [6]: 5
            'Generation'                        [7]: 1 #? must be 1 or greater to be a child
        ]
        # @note conversion syntax: child : Node = Node(csvrow[1],None,csvrow[5],csvrow[6],csvrow[6])  # create a node from the list

        """
        # @note conditons to be met to create and emplace the child node into the parent node's children dictionary:
        # treekey of csvrow MUST match parent for a Node to be created from it
        # 'Parent_of_Ingredient' must not be None and must the ingredient of Parent
        # 'Ingredient_Alias' must not be 'In' any Node with in the tiems of the parent's children dictionary
        # also an exact copy of this node cannot be already linked to the parent!
        if len(csvrow) != 8:  # if the csvrow is the proper length
            # raise a value error
            raise ValueError(
                'csvrow is not the proper length; the list passes contains the following:', csvrow)
        #! keep add conditon checks as progress on this test is made
        print(csvrow)
        # @note parse out any underscore characters from the ingredient and the parent of the ingredient to match the ingredient and parent of the node
        # remove any underscores from the ingredient
        csvrow[1] = csvrow[1].replace('_', ' ')
        # remove any underscores from the parent of the ingredient
        csvrow[3] = csvrow[3].replace('_', ' ')
        foundemplacelocation: bool = parent.treekey == csvrow[0] and csvrow[
            3] != 'None' and csvrow[3] == parent.ingredient and csvrow[7] > 0 and parent is not None
        if foundemplacelocation:
            # @audit somewhere in the project it needs to be determined if the user will allow the amount on hands from the csv file to be used or if the user will input the amount on hand themselves
            Node(csvrow[1], parent=parent, amountneeded=csvrow[6], amountofparentmadepercraft=csvrow[5],
                 amountonhand=csvrow[4], treekey=csvrow[0])  # create a node from the list
            return True
        else:
            return False

    def locate_emplace_spot(self, parent: Node, row: list):
        # try to emplace the node into the parent node's children dictionary
        spotfound: bool = self.emplacelink(parent, row)
        if not spotfound:
            for child in parent.children.items():
                self.locate_emplace_spot(child[1], row)
        else:
            if parent is not None:
                pass
                
    def test_headnodecreation(self,foundheadnodes : dict = test_pandacsvparsesearch())->Node:
        """
        test that the head node is created correctly
        """
        # call csv parse method and get a dictionary of head nodes
        # if it returns {-1:None} or the file is not in the directory, skip the test
        # else, open the file in read mode and check for nodes in the csv that match the value of the head node's key in the dictionary,
        # is not a head node instance (avoid duplicating the same nodes as dictionized nodes) and emplace nodes into the head node's tree
        
        #!foundheadnodes: dict = self.test_pandacsvparsesearch()
        if foundheadnodes == {-1: None} or not os.path.exists(path=TESTFILENAME):
            # @audit-info in the solution module the user would input an integer to the function to specify which head node to create and return, for this test return a random one
            self.skipTest('the csv file does not exist')
            return Node('NaNNodeName', None, -1, -1, -1)
        else:  # todo create tree rom csv file
            # open the file in read mode and check for nodes in the csv that match the value of the head node's key in the dictionary,
            # when you need to create a new node from the csv file
            # create a function that takes in a dictionary that stores the row of data and the head node instace,
            # the function should search through all the subnodes of the node parameter instance and figure out where to link the node instance created from the csv
            # these are the following condition for the found nodes: (red is the found node, blue is the node being emplaced)
            # red and blue's node treekeys are the same
            # red's parent ingredient is the same as blue's ingredient
            # get a random head node from the dictionary of head nodes
            returnhead: Node = random.choice(list(foundheadnodes.items()))[1]
            # @audit-info assert that the population of the tree is equal to the population of the mock tree
            #! call the function that figures out where to link the node and emplace it into the tree
            # open the file and read the rows to create a list of rows with matching treekeys as the selected node
            sublist: list = []  # ? list of rows that match the head node's tree key
            prevlistval: list = []
            # iterate through the rows of the dataframe
            for purple in pandas.read_csv(TESTFILENAME).to_dict('index').items():
                # convert the values of the dictionary to a list
                green: list = list(purple[1].values())
                # todo format ingredient alias to match the ingredient (rowlist[3] == rowlist[1])
                #!green[3] = green[1]
                # if the tree key of the row matches the head node's tree key
                if green[0] == returnhead.treekey:
                    sublist.append(green)
                # for each row, check if the it meets the conditions to be a child node of the head node
            for row in sublist:
                self.locate_emplace_spot(returnhead, row)
                # if it does not, check to see if any of the children meet the condition
            nodecount: int = self.countpopulation(returnhead)
# @note not needed anymore            self.assertEqual(nodecount,10)  # assert that the population of the tree is equal to the population of the mock tree
            # print the head node
            print('the returned tree is for', returnhead.ingredient)
            self.skipTest('not needed anymore')
            return returnhead  # return a random head node instance

    # todo append a list of attributes that do not match to the fail msg string of the tuple
    def istreesame(self, primetree: Node, derivedtree: Node) -> tuple:
        """return false if one attribute of the node is not the same value, treekeys do not count

        Args:
            red (Node): ingredient tree A
            blue (Node): ingredient tree B

        Returns:
            bool: returns true if any attribute value of any of the compared nodes are not the same in their respective ingredient trees
        """
        # @audit-info the trees created from the csv file are not correclty created in order if they duplicate ingredient names
        # check if the children dicts have the same amount of keys
#       if self.countpopulation(presetingredienttree) != self.countpopulation(csvsourcedtree):
#           print('population not the same')  # debug
#           return False
#           pass
        # submethod definitions
        if primetree.ingredient != derivedtree.ingredient:
            print('ingredients not the same')  # debug
            return (False, 'ingredients not the same')
        elif len(primetree.children) is not len(derivedtree.children):
            print('children not the same')
            return (False, 'children not the same')
        elif primetree.generation != derivedtree.generation:
            print('generations not the same')
            return (False, 'generations not the same')
        elif primetree.amountofparentmadepercraft != derivedtree.amountofparentmadepercraft:
            #            print('amounts not the same')  # debug
            pass
            return (False, 'amount of', primetree.ingredient, 'made per craft (', primetree.amountofparentmadepercraft, ')is not the same as', derivedtree.ingredient, '(', derivedtree.amountofparentmadepercraft, ')in the csv file')  # debug
        elif primetree.amountneeded != derivedtree.amountneeded:
            print('amounts not the same')  # debug
            return (False, 'amount needed to create the parent ingredient once is not the same')
        elif primetree.treekey == derivedtree.treekey:
            return (False, 'the keys of the tree are not the same')
        else:
            for index, node in enumerate(primetree.children.items()):
                # print the name of the node
                return self.istreesame(list(primetree.children.items())[index][1], list(derivedtree.children.items())[index][1])
            return (True, 'trees are the same')

    def returnlist(self, noctis: Node, minimus: list) -> list[tuple[int, int]]:
        """
        return a list of tuples (int,int):

        Args:
            [0] is the amount of parent made per craft of the node

            [1] is the amount needed to create the parent ingredient once

            [2] the generation of the Node
        """
        minimus.append((noctis.amountofparentmadepercraft,
                       noctis.amountneeded, noctis.generation))
        for child in noctis.children.items():
            # return a list of tuples (int,int): [0] is the amount of parent made per craft of the node [1] is the amount needed to create the parent ingredient once
            self.returnlist(child[1], minimus)
        return minimus

    def test_createdtreeissame(self):
        # uraniumrod            : Node = Node('uranium rod', self.pixels, 0, 500, 1)  # create a node instance with the name pixels and the parent node battery
        # get the head node of the test tree
        testhead: Node = self.test_headnodecreation()
        # @note assert that the tree created from the csv file is the same as the tree created from the mock tree
        assertvalue: tuple = self.istreesame(self.industrial_battery, testhead)
        # assert that the tree created from the csv file is the same as the tree created from the mock tree
        self.assertTrue(assertvalue[0], assertvalue[1])

    def test_comparelist(self):
        """
        compares a list of tuples 3 attributes between two trees, tree A being from the preset one and tree B being from the csv file
        the tuple contains the following attributes:

        [0] is the amount of parent made per craft of the node

        [1] is the amount needed to create the parent ingredient once

        [2] the generation of the Node
        """
        # uraniumrod            : Node = Node('uranium rod', self.pixels, 0, 500, 1)  # create a node instance with the name pixels and the parent node battery
        bordo: list = self.returnlist(self.industrial_battery, [])
        # get the head node of the test tree
        azureus: list = self.returnlist(self.test_headnodecreation(), [])
        # assert that the tree created from the csv file is the same as the tree created from the mock tree
        self.assertListEqual(
            azureus, bordo, '\nthe lists are not the same:\n\tList A: '+str(bordo)+'\n\tList B: '+str(azureus))

    def test_convertdepreciatedcsv(self, nameofoldcsv: str = 'convertme.csv') -> dict:
        """
        Convert depreciated csv file to pandas DataFrame
        return a dictionary of ingredient trees from the old csv file
        @note example of a row of a head node instance in the old csv file
        OLDFEILDNAMES = [
            'Ingredient',                   [0]: 'Head Item'
            'Parent_Ingredient',            [1]: 'None'
            'FAKE INGREDIENT NICKNAME',     [2]: 'None'  # this is the fake ingredient nickname @note inserted into the fields as a dummy value to match
            'Amount_on_Hand',               [3]: '0'
            'Amount_Made_Per_Craft',        [4]: '1'
            'Amount_Needed',                [5]: '1'
            'Generation',                   [6]: '0'
            'Tree_Key'                      [7]: '6eTrOuww5CfYq1rI'
        ]
        @note example of a row of a child node instance in the old csv file
        OLDFEILDNAMES = [
            'Ingredient',                   [0]: 'Whitespine'
            'Parent_Ingredient',            [1]: 'Sulphuric_Acid'
            'FAKE INGREDIENT NICKNAME',     [2]: 'Sulphuric Acid Nickname'  # this is the fake ingredient nickname
            'Amount_on_Hand',               [3]: '9999'
            'Amount_Made_Per_Craft',        [4]: '1'
            'Amount_Needed',                [5]: '2'
            'Generation',                   [6]: '2'
            'Tree_Key'                      [7]: '6eTrOuww5CfYq1rI'
        ]

        """
        panda: dict = {}  # dictionary of new nodes
        # read the csv file
        OLDFIELDNAMES = [
            'Ingredient',
            'Parent_Ingredient',
            'Amount_on_Hand',
            'Amount_Made_Per_Craft',
            'Amount_Needed',
            'Generation',
            'Tree_Key'
        ]
        # read the csv file and convert it to a dictionary of records
        for purplepanda in pandas.read_csv(nameofoldcsv, names=OLDFIELDNAMES).to_dict('index').items():
            # convert the record to a list
            oxygen: list = list(purplepanda[1].values())
            """
            @note field names/value models from the old csv file
            fieldnames = [                
                [0]: 'Ingredient':'Focusing Array',     # the name of the ingredient
                [1]: 'Parent_Ingredient':'None'         # the parent ingredient of the node
                [2]: 'Amount_on_Hand':'1'               # the amount of the ingredient on hand
                [3]: 'Amount_Made_Per_Craft':'1'        # the amount of the parent ingredient made per craft
                [4]: 'Amount_Needed':'1'                # the amount needed to create the parent ingredient once
                [5]: 'Generation':'0'                   # the generation of the node
                [6]: 'Tree_Key:'UoPydLI98vet9sUb'       # the key of the tree the node belongs to
            ]
            """
            if oxygen[1] == 'None' and oxygen[3] == '1' and oxygen[4] == '1' and oxygen[5] == '0':
                panda.update({oxygen[6]: Node(parent=None, ingredient=oxygen[0], amountofparentmadepercraft=oxygen[3],
                             amountneeded=oxygen[4], treekey=oxygen[6])})  # create a head node and add it to the dictionary of nodes
        # assert that the dictionary is not empty and not equal {-1:None}
        self.assertTrue(len(panda) >= 1 and panda != {-1: None})
        if len(panda) == 0:
            return {-1: None}
        else:
            # parse the csv file and create trees from the nodes
            for headnode in panda.items():
                pinkpandarows: list = []
                # read the csv file and convert it to a dictionary of records
                for pinkpanda in pandas.read_csv(nameofoldcsv, names=OLDFIELDNAMES).to_dict('index').items():
                    # convert the record to a list
                    pinkerpanda: list = list(pinkpanda[1].values())
                    if pinkerpanda[6] == headnode[0]:
                        pinkpandarows.append(pinkerpanda)
                for nani in pinkpandarows:
                    # insert a fake ingredient_alias attribute into the list 2nd element of the each row
                    # insert a fake ingredient_alias attribute into the list 2nd element of the each row
                    nani.insert(2, 'NO_ALIAS')
                # @note reorganize so that the fields of this csv match the fields of the newer csv positonally
                for nani in pinkpandarows:
                    # @note swap 1 ingredient and treekey (0,7)
                    nani[0], nani[7] = nani[7], nani[0]
                    # @note swap 2 ingredient and parent_ingredient (7,1)
                    nani[7], nani[1] = nani[7], nani[1]
                    # @note swap 3 generation and parent_ingredient (7,5)
                    nani[7], nani[5] = nani[7], nani[5]
                    # @note swap 4 parent_ingredient and needed (6,5)
                    nani[6], nani[5] = nani[6], nani[5]
                    # @note swap 5 parent_ingredient and made (5,4)
                    nani[5], nani[4] = nani[5], nani[4]
                    # @note swap 6 parent_ingredient and onhand (4,3)
                    nani[4], nani[3] = nani[4], nani[3]
                    # swap 1 and 7
                    nani[1], nani[7] = nani[7], nani[1]  # swap 1 and 7
                    nani[7], nani[2] = nani[2], nani[7]  # swap 7 and 2
                    nani[6], nani[7] = nani[7], nani[6]  # swap 6 and 7
                    nani[6], nani[5] = nani[5], nani[6]  # swap 6 and 5
                    nani[5], nani[4] = nani[4], nani[5]  # swap 5 and 4
                    nani[3], nani[4] = nani[4], nani[3]  # swap 3 and 4`
                    nani[3], nani[2] = nani[2], nani[3]  # swap 3 and 2
                    # @note convert numberic data into integers
                    ariana: int = 4
                    # ariana 3 is less than 7
                    while ariana < 8:
                        if not nani[ariana].isdigit():
                            # raise a value error if the value is not a digit
                            raise ValueError('not a digit')
                        else:
                            # convert the amount on hand to an integer
                            nani[ariana] = int(nani[ariana])
                        ariana += 1  # increment ariana by 1
                # create a tree from the rows
                for pink in pinkpandarows:
                    # locate the spot to place the node and place it
                    self.locate_emplace_spot(headnode[1], pink)
            #! for debugging, output the population of each head node in the dictionary
            for node in panda.items():
                # print the head node key and the population of the tree
                print(node[0], '-', node[1].ingredient,
                      ':', self.countpopulation(node[1]))
            return panda  # @note use the dictionary to print the tree to the new csv file
        # self assert that the dictionary is not empty and not equal {-1:None}

    def test_checkforduplicatetrees(self,head : Node=thorium_rod)->tuple:
        """
        test that there are exact copies of an ingredient tree written into csv file
        """
        # check if the file is in the current directory, if is not, skip the test
        if not os.path.isfile(TESTFILENAME):
            self.skipTest('test.csv not found')
            return (False,'test.csv not found')
        elif  len(self.test_pandacsvparsesearch()) == 0:
            self.skipTest('no head nodes found')
            return (False,'no head nodes found')
            # if the file exists in the current direct
        else:
            duplicatetree : bool = False
            # check that the node passed into the function is a head node
            if head.parent is not None:
                while head.parent is not None:
                    head = head.parent

            #! check for the head nodes in the csv file
            headnodes : dict = self.test_pandacsvparsesearch()
            #check if any of the head nodes match the ingredient name of that the head node of the tree passed into the method
            checkthesenodes : dict = {}
            for node in headnodes.items():
                # parse the returned list of head nodes for any head nodes that match the name of the head node of the tree passed into the method
                if node[1].ingredient == head.ingredient:
                    checkthesenodes.update({node[0]:node[1]})
            if len(checkthesenodes) == 0:
                self.skipTest('No head nodes matching the ingredient of the passed parameter head node were found')
                return (False,'No head nodes matching the ingredient of the passed parameter head node were found')
            else:
                # create trees from each node in the checkthesenodes dictionary
                for node in checkthesenodes.items():
                    # create a tree from the head node
                    self.test_pandacsvparsesearch(node[0])
                    # check if the tree created from the head node matches the tree passed into the method
                    if self.comparetrees(node[1],head):
                        duplicatetree = True
                        break
                    else:
                        duplicatetree = False
                self.assertTrue(duplicatetree)
                return (True,'duplicate tree found')


if __name__ == '__main__':
    blue = CSVsutilization()  # create an instance of the class
    for red in blue.test_pandacsvparsesearch().items():
        print(red[0], ':', red[1], ':', red[1].ingredient)
#!    print('')
#!    yellow : Node = blue.test_headnodecreation()
#!    for headnode in blue.test_convertdepreciatedcsv().items():
#!        blue.test_pandascsvwrite(headnode[1])  # write the tree to the new csv file
