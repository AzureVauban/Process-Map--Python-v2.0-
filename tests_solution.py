"""
Unit Tests for the solution.py module
"""
import os
import unittest
import random
import pandas
from zmq import PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_INITIATE
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
    @classmethod
    def treekeymismatch(cls):
        return "Tree key mismatch"


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
    def countpopulation(self,node : Node, count : int = 0) -> int:
            """
            count how many subnodes are connected parameter node
            @audit-info use a recursive function to count the population of the tree, start off with the head node!
            Args:
                node (Node): node to count the subnodes of
                count (int, optional): integer number of counted nodes. Defaults to 0.

            Returns:
                int: population of the node's tree
            """
            count +=1
            if len(node.children.items()) > 0:
                for child in node.children.items():
                    count = self.countpopulation(child[1],count)
            return count
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

    def test_pandacsvparsesearch(self)->dict: # todo turn this into a function in the solution module when this unit test passes 
        """
        test parsing the csv file to find head node instances
        
        if file does not exist, skip the test (in the solution module return {-1:None} instead)
        if the file already exists, open it in read mode
            parse the csv file to see if there are any rows of data that match the 
            conditions of a head node instance, if they do create a head node instance and add it into a returnable dict
        """
        if not os.path.exists(TESTFILENAME):
            self.skipTest(exep_msg.csvnotexist())  # skip the test
            return {-1: None}  # return a dict with a key of -1 and a value of None
        else:
            # value is the treekey and the item is the headnode translated from the csv file
            foundheadpoints: dict = {}
            # turn a row of the csv data into a dictionary
            # @audit-info convert row into a list, use a boolean to detect if the nesscary values are present in the proper positions of the list to match a head node of the tree, and if it does input it the dictionary of head nodes
            # @audit-info headinstance condition is met if list[index=3] is None, list[index=5] = 1, list[index=6] = 1, adn list[index=7] = 0
            for purple in pandas.read_csv(TESTFILENAME).to_dict('index').items():  # iterate through the rows of the dataframe
                green : list = list(purple[1].values())  # convert the values of the dictionary to a list
                #todo format ingredient alias to match the ingredient (rowlist[3] == rowlist[1])
                #!green[3] = green[1]
                # @note conversion syntax: yellow : Node = Node(green[1],None,green[5],green[6],green[6])  # create a node from the list
                # @note isheadinstance: bool = green[3] == 'None' and green[5] == 1 and green[6] == 1 and green[7] == 0
                if green[3] == 'None' and green[5] == 1 and green[6] == 1 and green[7]== 0:  # if the conditions are met for it to mock a head node
                    # create a node from the row's data
                    foundheadpoints.update({green[0]: Node(green[1], None, green[4], green[5], green[6],False,False,green[0])})  # add the node to the dictionary of head nodes
                    print('found a node!')  #!delete this later
                # @note when this is turned into a function, if the returned dictionary is empty, return {-1:None} instead of an empty dictionary
            #check that the key of the dictionary and the treekey of the node are the same, if they are not, raise an exception
            for key, value in foundheadpoints.items():
                if key != value.treekey:
                    raise ValueError(exep_msg.treekeymismatch())
            self.assertGreaterEqual(len(foundheadpoints), 1, 'No headnodes found')  # assert that the headnodes are found
            return foundheadpoints  # return the headnodes
         
    def emplacelink(self,parent : Node, csvrow : list) -> bool:
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
            raise ValueError('csvrow is not the proper length; the list passes contains the following:',csvrow)  # raise a value error
        #! keep add conditon checks as progress on this test is made
        if parent.treekey == csvrow[0] and csvrow[3] != 'None' and csvrow[3] == parent.ingredient and csvrow[7] > 0:
            #@audit somewhere in the project it needs to be determined if the user will allow the amount on hands from the csv file to be used or if the user will input the amount on hand themselves
            child : Node = Node(csvrow[1],parent,csvrow[5],csvrow[6],csvrow[6],False,False,csvrow[0])  # create a node from the list
            return True
        else:
            return False
    def locate_emplace_spot(self,parent : Node,row : list):
        spotfound : bool = self.emplacelink(parent,row)  # try to emplace the node into the parent node's children dictionary
        if not spotfound:
            for child in parent.children.items():
                self.locate_emplace_spot(child[1],row)
   
    
    
    def test_headnodecreation(self):
        """
        test that the head node is created correctly
        """
        # call csv parse method and get a dictionary of head nodes
        # if it returns {-1:None} or the file is not in the directory, skip the test
        # else, open the file in read mode and check for nodes in the csv that match the value of the head node's key in the dictionary,
            # is not a head node instance (avoid duplicating the same nodes as dictionized nodes) and emplace nodes into the head node's tree
        foundheadnodes : dict = self.test_pandacsvparsesearch()
        if foundheadnodes == {-1:None} or not os.path.exists(path=TESTFILENAME):
            # @audit-info in the solution module the user would input an integer to the function to specify which head node to create and return, for this test return a random one
            self.skipTest(exep_msg.csvnotexist())
            return Node('NaNNodeName',None,-1,-1,-1) 
        else: #todo create tree rom csv file
            # open the file in read mode and check for nodes in the csv that match the value of the head node's key in the dictionary,
            # when you need to create a new node from the csv file
            # create a function that takes in a dictionary that stores the row of data and the head node instace,
                # the function should search through all the subnodes of the node parameter instance and figure out where to link the node instance created from the csv
                # these are the following condition for the found nodes: (red is the found node, blue is the node being emplaced)
                    # red and blue's node treekeys are the same
                    # red's parent ingredient is the same as blue's ingredient
            returnhead : Node = random.choice(list(foundheadnodes.items()))[1]  # get a random head node from the dictionary of head nodes
            # @audit-info assert that the population of the tree is equal to the population of the mock tree
            #! call the function that figures out where to link the node and emplace it into the tree
            # open the file and read the rows to create a list of rows with matching treekeys as the selected node
            sublist : list = []  #? list of rows that match the head node's tree key
            prevlistval : list = []
            for purple in pandas.read_csv(TESTFILENAME).to_dict('index').items():  # iterate through the rows of the dataframe
                green : list = list(purple[1].values())  # convert the values of the dictionary to a list
                #todo format ingredient alias to match the ingredient (rowlist[3] == rowlist[1])
                #!green[3] = green[1]
                if green[0] == returnhead.treekey:  # if the tree key of the row matches the head node's tree key
                    sublist.append(green)
                # for each row, check if the it meets the conditions to be a child node of the head node
            for row in sublist:
                self.locate_emplace_spot(returnhead,row)
                # if it does not, check to see if any of the children meet the condition 
            nodecount : int = self.countpopulation(returnhead)
            self.assertEqual(nodecount,10)  # assert that the population of the tree is equal to the population of the mock tree 
            return returnhead  # return a random head node instance
    def istreesame(self,red : Node, green : Node) -> bool:
        """return false if one attribute of the node is not the same value, treekeys do not count

        Args:
            red (Node): ingredient tree A
            blue (Node): ingredient tree B

        Returns:
            bool: returns true if any attribute value of any of the compared nodes are not the same in their respective ingredient trees
        """
        def tentativemethod2(self,apple : list[Node],pear: list[Node]): #todo change the name of the subfunction
            print('list A',apple)
            print('list B',pear)
            for appleseed in apple:
                if not isinstance(appleseed,Node):
                    raise TypeError('an item of the list is not an instance if',Node)  # raise a type error

            for pearseed in pear:
                if not isinstance(pearseed,Node):
                    raise TypeError('an item of the list is not an instance if',Node)  # raise a type error
            if len(apple) != len(pear) :
                raise ValueError('the two lists are not the same length')  # raise a value error
            for index,node in enumerate(apple):
                self.istreesame(node,pear[index])  # call the function recursively to check the subnodes of the nodes
        # check if the children dicts have the same amount of keys
        if len(red.children) != len(green.children):
            return False
        else:
            redlist : list = list(red.children.items())  # convert the children dictionary to a list
            for index,value in enumerate(redlist):  # iterate through the list
                redlist[index] = value[1]  # convert the tuple to a node instance
            greenlist: list = list(green.children.items())  # convert the children dictionary to a list
            for index,value in enumerate(greenlist):  # iterate through the list
                greenlist[index] = value[1]  # convert the tuple to a node instance
            #!return self.istreesame.tentativemethod2(redlist,greenlist)  # call the subfunction to check the subnodes of the nodes
            for index,node in enumerate(redlist):
                self.istreesame(node,greenlist[index])  # call the function recursively to check the subnodes of the nodes
        
    def test_createdtreeissame(self):
        #mock tree
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
        #head node of test tree
        testhead : Node = self.test_headnodecreation()  # get the head node of the test tree
        #@note assert that the tree created from the csv file is the same as the tree created from the mock tree
        #! self.skipTest('Not implemented yet')  # skip the test if the csv file does not exist
        self.assertTrue(self.istreesame(industrial_battery,testhead),'the test tree created from the csv does not share attributes to the mock ingredient tree)  # assert that the tree created from the csv file is the same as the tree created from the mock tree')


if __name__ == '__main__':
    blue = CSVsutilization()  # create an instance of the class
    for red in blue.test_pandacsvparsesearch().items():
        print(red[0],':',red[1],':',red[1].ingredient)
    yellow : Node = blue.test_headnodecreation()
    print('\nNode:',yellow,'('+yellow.treekey+')')  # call the function to test the csv parsing and search method