"""
Unit Tests for the solution.py module
"""
import os
import unittest
import random
from numpy import minimum
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
    @classmethod
    def treekeymismatch(cls):
        return "Tree key mismatch"



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
    
    #@note mock ingredient tree for industral battery https://frackinuniverse.miraheze.org/wiki/Industrial_Battery
    @classmethod
    def countpopulation(cls,node : Node, count : int = 0) -> int:
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
                count = cls.countpopulation(child[1],count)
        return count
    industrial_battery    : Node = Node('industrial battery', None,treekey=Node.generate_treekey())
    protocite_bar         : Node = Node('protocite bar', industrial_battery, 0, 1, 5)
    protocite             : Node = Node('protocite', protocite_bar, 0, 1, 2)
    battery               : Node = Node('battery', industrial_battery, 0, 1, 2)
    pixels                : Node = Node('pixels', battery, 0, 1, 2500)
    quantum_processor     : Node = Node('quantum processor', industrial_battery, 0, 1, 1)
    silicon_board         : Node = Node('silicon board', quantum_processor, 0, 1, 4)
    protocite_bar2        : Node = Node('protocite bar', quantum_processor, 0, 1, 2)
    thorium_rod           : Node = Node('thorium rod', industrial_battery, 0, 1, 5)
    thorium_ore           : Node = Node('thorium ore', thorium_rod, 0, 1, 2)
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

    class SubMethods(): #todo finish creating methods
        """a class containing methods for returning a set of instance attributes from a head node
        """
        head : Node
        def __init__(self,head : Node) -> None:
            self.head = head
        @classmethod
        def ingredients(cls,monokai : Node,noctis : list) ->list:
            for child in monokai.children.items():
                cls.ingredients(child[1],noctis)  # recurse through the tree
            return noctis
        @classmethod
        def children(cls,monokai : Node,obscuro : list) -> list:
            for child in monokai.children.items():
                cls.ingredients(child[1],obscuro)  
            return obscuro
        @classmethod
        def generation(cls,monokai : Node,uva : list) -> list:
            for child in monokai.children.items():
                cls.ingredients(child[1],uva)  
            return uva
        @classmethod
        def amountneeded(cls,monokai : Node,viola : list)-> list:
            for child in monokai.children.items():
                cls.ingredients(child[1],viola)  
            return viola
        @classmethod
        def amountmadepercraft(cls,monokai : Node,lux : list)-> list:
            for child in monokai.children.items():
                cls.ingredients(child[1],lux)  
            return lux
        @classmethod
        def treekeys(cls,monokai : Node,lilac : list)-> list:
            for child in monokai.children.items():
                cls.ingredients(child[1],lilac)  
            return lilac
        @classmethod
        def amountonhand(cls,monokai : Node,hibernus : list)-> list: #@note for debugging purposes
            for child in monokai.children.items():
                cls.ingredients(child[1],hibernus)  
            return hibernus
        
    
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
       
        if not os.path.exists(TESTFILENAME):
            # create the file
            pandas.DataFrame(columns=FIELDNAMES).to_csv(TESTFILENAME, index=False)
            self.test_pandascsvwrite()  # call the function again to write to the file
            self.skipTest(exep_msg.csvnotexist())  # skip the test
        else:
            # write preset mock ingredient tree onto it
            for line in self.industrial_battery.create_csv_writerows([]):
                pandas.DataFrame(line, index=[0]).to_csv(TESTFILENAME, mode='a', header=False, index=False)
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
                
                # @note conversion syntax: yellow : Node = Node(green[1],None,green[5],green[6],green[6])  # create a node from the list
                # @note isheadinstance: bool = green[3] == 'None' and green[5] == 1 and green[6] == 1 and green[7] == 0
                if green[3] == 'None' and green[5] == 1 and green[6] == 1 and green[7]== 0:  # if the conditions are met for it to mock a head node
                    # create a node from the row's data
                    foundheadpoints.update({green[0]: Node(green[1], None, green[4], green[5], green[6],False,False,green[0])})  # add the node to the dictionary of head nodes
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
        foundemplacelocation : bool = parent.treekey == csvrow[0] and csvrow[3] != 'None' and csvrow[3] == parent.ingredient and csvrow[7] > 0 and parent is not None
        if foundemplacelocation:
            #@audit somewhere in the project it needs to be determined if the user will allow the amount on hands from the csv file to be used or if the user will input the amount on hand themselves
            #!child : Node = Node(csvrow[1],parent,csvrow[5],csvrow[6],csvrow[6],False,False,csvrow[0])  # create a node from the list
            Node(csvrow[1],parent=parent,amountneeded=csvrow[6],amountofparentmadepercraft=csvrow[5],amountonhand=csvrow[4],treekey=csvrow[0])  # create a node from the list
            return True
        else:
            return False
        
        
    def locate_emplace_spot(self,parent : Node,row : list):
        spotfound : bool = self.emplacelink(parent,row)  # try to emplace the node into the parent node's children dictionary
        if not spotfound:
            for child in parent.children.items():
                self.locate_emplace_spot(child[1],row)
        else:
            if parent is not  None:
                pass
   
    
    
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
#@note not needed anymore            self.assertEqual(nodecount,10)  # assert that the population of the tree is equal to the population of the mock tree 
            print('the returned tree is for',returnhead.ingredient)  # print the head node
            return returnhead  # return a random head node instance
            self.skipTest('not needed anymore')
        
        
    def istreesame(self,primetree : Node, derivedtree : Node) -> tuple: #todo append a list of attributes that do not match to the fail msg string of the tuple
        """return false if one attribute of the node is not the same value, treekeys do not count

        Args:
            red (Node): ingredient tree A
            blue (Node): ingredient tree B

        Returns:
            bool: returns true if any attribute value of any of the compared nodes are not the same in their respective ingredient trees
        """
        #@audit-info the trees created from the csv file are not correclty created in order if they duplicate ingredient names
        # check if the children dicts have the same amount of keys
#       if self.countpopulation(presetingredienttree) != self.countpopulation(csvsourcedtree):
#           print('population not the same')  # debug
#           return False
#           pass
        # submethod definitions
        if primetree.ingredient != derivedtree.ingredient:
            print('ingredients not the same')  # debug
            return (False,'ingredients not the same')
        elif len(primetree.children) is not len(derivedtree.children):
            print('children not the same')
            return (False,'children not the same')
        elif primetree.generation != derivedtree.generation:
            print('generations not the same')
            return (False,'generations not the same')
        elif primetree.amountofparentmadepercraft != derivedtree.amountofparentmadepercraft:
#            print('amounts not the same')  # debug
            pass
            return (False,'amount of',primetree.ingredient,'made per craft (',primetree.amountofparentmadepercraft,')is not the same as',derivedtree.ingredient,'(',derivedtree.amountofparentmadepercraft,')in the csv file')  # debug
        elif primetree.amountneeded != derivedtree.amountneeded:
            print('amounts not the same')  # debug
            return (False, 'amount needed to create the parent ingredient once is not the same')
        elif primetree.treekey == derivedtree.treekey:
            return (False, 'the keys of the tree are not the same')
        else:
            for index,node in enumerate(primetree.children.items()):
                return self.istreesame(list(primetree.children.items())[index][1],list(derivedtree.children.items())[index][1])  # print the name of the node
            return (True,'trees are the same')        
    
    def returnlist(self,noctis : Node, minimus : list)-> list[tuple[int,int]]:
        """
        return a list of tuples (int,int):
            
        Args:
            [0] is the amount of parent made per craft of the node
            
            [1] is the amount needed to create the parent ingredient once
            
            [2] the generation of the Node
        """
        minimus.append((noctis.amountofparentmadepercraft,noctis.amountneeded,noctis.generation))
        for child in noctis.children.items():
            self.returnlist(child[1],minimus)  # return a list of tuples (int,int): [0] is the amount of parent made per craft of the node [1] is the amount needed to create the parent ingredient once
        return minimus
    
    def test_createdtreeissame(self):
        #uraniumrod            : Node = Node('uranium rod', self.pixels, 0, 500, 1)  # create a node instance with the name pixels and the parent node battery
        # get the head node of the test tree
        testhead: Node = self.test_headnodecreation()
        #@note assert that the tree created from the csv file is the same as the tree created from the mock tree
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
        #uraniumrod            : Node = Node('uranium rod', self.pixels, 0, 500, 1)  # create a node instance with the name pixels and the parent node battery
        bordo: list = self.returnlist(self.industrial_battery, [])
        # get the head node of the test tree
        azureus: list = self.returnlist(self.test_headnodecreation(), [])
        # assert that the tree created from the csv file is the same as the tree created from the mock tree
        self.assertListEqual(
            azureus, bordo, '\nthe lists are not the same:\n\tList A: '+str(bordo)+'\n\tList B: '+str(azureus))

    def test_checkforduplicatetrees(self):
        """
        test that there are exact copies of an ingredient tree written into csv file
        """
        # check if the file is in the current directory, if is not, skip the test
        if not os.path.isfile(TESTFILENAME):
            self.skipTest('test.csv not found')
        else:
            pass
        # if the file exists in the current directory read it and parse for head nodes
            # if it has only one head node, skip the test
            # close the file
        # if more than one head node, run the test
            # open the file and parse it for head nodes
            # if head nodes have matching ingredient names, create an ingredient tree and then compare the trees using the istreesame method
            # assert true if the trees are the same, assert false if the trees are not the same
            # close the file
        self.skipTest('test not implemented')  # skip the test
    
    def test_convertdepreciatedcsv(self,nameofoldcsv: str = 'convertme.csv') -> dict:
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
        panda : dict = {} # dictionary of new nodes
        # read the csv file
        OLDFEILDNAMES = [
            'Ingredient',               
            'Parent_Ingredient',
            'Amount_on_Hand',
            'Amount_Made_Per_Craft',
            'Amount_Needed',
            'Generation',
            'Tree_Key'    
        ]
        for purplepanda in pandas.read_csv(nameofoldcsv, names=OLDFEILDNAMES).to_dict('index').items():  # read the csv file and convert it to a dictionary of records
            oxygen : list = list(purplepanda[1].values())  # convert the record to a list
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
                panda.update({oxygen[6]:Node(parent=None,ingredient=oxygen[0],amountofparentmadepercraft=oxygen[3],amountneeded=oxygen[4],treekey=oxygen[6])})  # create a head node and add it to the dictionary of nodes
        self.assertTrue(len(panda)>=1 and panda != {-1:None})  # assert that the dictionary is not empty and not equal {-1:None}
        if len(panda) == 0:
            return {-1:None}
        else:
            # parse the csv file and create trees from the nodes
            for headnode in panda.items():
                pinkpandarows: list = []
                for pinkpanda in pandas.read_csv(nameofoldcsv, names=OLDFEILDNAMES).to_dict('index').items():  # read the csv file and convert it to a dictionary of records
                    pinkerpanda : list = list(pinkpanda[1].values())  # convert the record to a list
                    if pinkerpanda[6] == headnode[0]:
                        pinkpandarows.append(pinkerpanda)
                for nani in pinkpandarows:
                    # insert a fake ingredient_alias attribute into the list 2nd element of the each row
                    nani.insert(2, 'Nani')  # insert a fake ingredient_alias attribute into the list 2nd element of the each row
                #@note reorganize so that the fields of this csv match the fields of the newer csv positonally
                for nani in pinkpandarows:
                    # swap the first and the last element of the list
                    nani[0],nani[6] = nani[6],nani[0]  # swap the first and the last element of the list
                # create a tree from the rows
                for pink in pinkpandarows:
                    self.locate_emplace_spot(headnode[1], pink)  # locate the spot to place the node and place it  
            # sort dictionary of head nodes based on the size of each tree
            #! for debugging, output the population of each head node in the dictionary
            for node in panda.items():
                print(node[0],'-',node[1].ingredient,':',self.countpopulation(node[1]))  # print the head node key and the population of the tree
            return panda #@note use the dictionary to print the tree to the new csv file
        #self assert that the dictionary is not empty and not equal {-1:None}
if __name__ == '__main__':
    blue = CSVsutilization()  # create an instance of the class
    for red in blue.test_pandacsvparsesearch().items():
        print(red[0],':',red[1],':',red[1].ingredient)
    yellow : Node = blue.test_headnodecreation()