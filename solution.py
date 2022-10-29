"""
main script for Python Process Map (v2.0)
Changes from v1.0:
- outputting data to a .csv file for later use
- inputting data to a .csv file for utilization
- search for a node in the tree and copy it instead of retyping all your data
- inputting basic arithmetic symbols when prompted to input numeric data (not added yet)
"""
import csv
import math
import os
import random
import sys
import time

PROGRAMMODETYPE: int = 0
CSVFILENAME: str = 'ingredient_tree_TENTATIVENAME.csv'
FIELDNAMES: list = [  # list of field names for the csv output file
    'Tree_Key',  # 74nry8keki',
    'Ingredient',  # Copper Wire
    'Ingredient_Alias',  # Copper_Wire__ZpgMzAwQdfRu
    'Parent_of_Ingredient',  # Silicon Board
    'Amount_on_Hand',  # 0
    'Amount_Of_Parent_Made_Per_Craft',  # 9
    'Amount_Needed_Per_Craft',  # 0
    'Generation'  # 1
]
#! revert this modification of the filename when finished utilizing it for testing
GLOBALNODEDICT: dict = {}  # {instancekey: Node}


def generatename(lengthlimit: int = random.randint(10, 20)) -> str:
    """randomly generations a return string of a random length between 10 and 20 characters

    Returns:
        str: randomly generated string
    """
    # create a random name as a string
    yuggoth: str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    mocknodename: str = ''
    for _ in range(random.randint(6, lengthlimit)):
        mocknodename += random.choice(yuggoth)
    return mocknodename


class NodeB:
    """
    class for storing simple data about an item such as its name and how much is needed to create
    its parent
    """
    ingredient: str = ''
    aliasingredient: str = ''
    #! if the ingredient name has been repeated somewhere else in the
    #! tree, make the aliasingredient a unique name and output into the csv file
    amountonhand: int = 0
    amountneeded: int = 0
    amountofparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, ingredient: str = '', amountonhand: int = 0, amountofparentmadepercraft: int = 1, amountneeded: int = 1) -> None:
        """
        Args:
            name (str, optional): name of the item. Defaults to ''.
            red (int, optional): amount of the item you have on hand. Defaults to 0.
            blue (int, optional): amount of the parent item you create each time you craft it.
            Defaults to 1.
            yellow (int, optional): amount of item needed to craft the parent item one time.
            Defaults to 1.
        """
        if not isinstance(amountonhand,int):
            raise TypeError('amountonhand must be an integer not a '+str(type(amountonhand)))
        if not isinstance(amountofparentmadepercraft,int):
            raise TypeError('amountofparentmadepercraft must be an integer not a ' + str(type(amountofparentmadepercraft)))  #! add a check for float and convert to int if necessary
        if not isinstance(amountneeded,int):
            raise TypeError('amountneeded must be an integer not a ' + str(type(amountneeded)))
        self.amountonhand = amountonhand
        self.amountofparentmadepercraft = amountofparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.aliasingredient = self.ingredient
        self.amountresulted = 0


class Node(NodeB):
    """
    stores identifiable features of an item, such as the parent and children instances
    Args:
        NobeB (class): parent class of item
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    askmadepercraftquestion: bool = False
    # this is unique identifer for an ingredient tree when its outputted into a csv file
    treekey: str = ''
    ismain_promptinputbool: bool = True

    def __init__(self, ingredient: str = '', parent=None, amountonhand: int = 0, amountofparentmadepercraft: int = 1, amountneeded: int = 1, green: bool = False, orange: bool = __name__ == '__main__',treekey: str = 'NanKey') -> None:  # pylint:disable=C0301
        """
        default constructor for Node instance, stores identifying features of an item's
        information

        Args:
            name (str, optional): name of the item. Defaults to ''.
            pare (class, optional): parent instance of declared Node. Defaults to None
            red (int, optional): amount of the item you have on hand. Defaults to 0.
            blue (int, optional): amount of the parent item you create each time you craft it.
            Defaults to 1.
            yellow (int, optional): amount of item needed to craft the parent item one time.
            Defaults to 1.
            green (bool,optional): boolean variable, checks if one of the Node's sibiling instances was prompted to input the amount made per craft (blue)
        """
        super().__init__(ingredient, amountonhand, amountofparentmadepercraft, amountneeded)
        self.instancekey = Node.instances
        self.children = {}
        self.ismain_promptinputbool = orange
        self.parent = parent
        if self.parent is not None and isinstance(self.parent, Node):
            self.generation = self.parent.generation + 1
            self.parent.children.update({self.instancekey: self})
            self.treekey = self.parent.treekey
            self.ismain_promptinputbool = self.parent.ismain_promptinputbool
            self.treekey = self.parent.treekey
        else:
            self.generation = 0
            self.treekey = self.generate_treekey()  # generate a unique tree key
        if not __name__ == '__main__' and parent is None:
            pass
        elif __name__ == '__main__' and parent is None:
            self.treekey = treekey
        # set tree key of this instance
      
        
        if not self.checkaliasuniqueness(self.aliasingredient):
            self.aliasingredient = self.aliasingredient + '__' + generatename()
        self.askmadepercraftquestion = green
        Node.instances += 1
        if self.ismain_promptinputbool:
            self.__inputnumerics()

    def __inputnumerics(self):
        """
        prompt input of the numeric data for the instance from the user
        """
        # prompt amount on hand
        while True and PROGRAMMODETYPE == 0:
            print('How much', self.ingredient, 'do you have on hand: ')
            self.amountonhand = promptint()
            if self.amountonhand < 0:
                print('That number is not valid')
            else:
                break
            # prompt amount needed
        if self.parent is not None:
            # prompt amount made per craft
            while True and self.askmadepercraftquestion:
                print('How much', self.parent.ingredient,
                      'do you create each time you craft it: ')
                self.amountofparentmadepercraft = promptint()
                if self.amountofparentmadepercraft < 1:
                    print('That number is not valid')
                else:
                    self.askmadepercraftquestion = False
                    break
            while True:
                print('How much', self.ingredient, 'do you need to craft',
                      self.parent.ingredient, '1 time: ')
                self.amountneeded = promptint()
                if self.amountneeded < 1:
                    print('That number is not valid')
                else:
                    break

    def clearamountresulted(self):
        """
        clear amount resulted for all subnodes below this instance
        """
        self.queueamountresulted.clear()
        if len(self.children) > 0:
            for child in self.children.items():
                if not isinstance(child[1], Node):
                    raise TypeError('Child is not an instance of', Node)
                child[1].clearamountresulted()
    # methods for creating and utilizing the .csv file

    # todo use in the constructor of the class
    def checkaliasuniqueness(self, checkstring: str) -> bool:
        """check to see if the ingredient name is present on another node in the tree

        Returns:
            bool: return true if the ingredient name is present on another node of the tree
        """
        if checkstring != self.ingredient and self.ingredient != self.aliasingredient:
            for child in self.children.items():
                child[1].checkaliasuniqueness(checkstring)
        return checkstring != self.ingredient and self.ingredient != self.aliasingredient

    @classmethod
    def generate_treekey(cls, length : int = random.randint(5,20)) -> str:
        """
        randomly generates an alpha numeric string to be used as a unique identifier for the tree
        and all nodes linked to this instance
        """
        cls.treekey = ''
        for _ in range(0, length):
            cls.treekey += random.choice(
                '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return cls.treekey
    # make a method to return a list with all the info needed on a line of the csv file
    def create_csv_writerow(self) -> dict:
        """
        FIELDNAMES: list = [  # list of field names for the csv output file
            'Tree_Key': 74nry8keki',
            
            'Ingredient': Copper Wire
            
            'Ingredient_Alias': Copper Wire__ZpgMzAwQdfRu
            
            'Parent_of_Ingredient': Silicon Board
            
            'Amount_on_Hand': 0
        
            'Amount_Made_Per_Craft': 9
            
            'Amount_Needed_Per_Craft': 0
            
            'Generation': 1
        ]
        Returns:
            dict: dictionary of all the information needed to be stored in the .csv file
        """
        azathoth: dict = {}
        ghast: str = 'None'
        # if the parent is not None, set the parent ingredient to the ingredient of the parent
        if self.parent is not None:
            ghast = self.parent.ingredient
        # input data into the dictionary 
        azathoth.update({FIELDNAMES[0]: self.treekey})
        azathoth.update({FIELDNAMES[1]: self.ingredient})
        azathoth.update({FIELDNAMES[2]: self.aliasingredient.replace(' ', '_')})
        azathoth.update({FIELDNAMES[3]: ghast})
        azathoth.update({FIELDNAMES[4]: str(self.amountonhand)})
        azathoth.update({FIELDNAMES[5]: str(self.amountofparentmadepercraft)})
        azathoth.update({FIELDNAMES[6]: str(self.amountneeded)})
        azathoth.update({FIELDNAMES[7]: str(self.generation)})
        return azathoth

    def create_csv_writerows(self, kraken: list) -> list:
        """
        create a list dictionaries of all the information needed to be stored in the .csv file for an ingredient tree
        rows = [
            {
            'Tree Key',  # 74nry8keki
            'Ingredient',  # Coal
            'Parent of Ingredient',  # Carbon
            'Amount on Hand',  # 0
            'Amount Made Per Craft',  # 1
            'Amount Needed Per Craft',  # 10
            'Generation'  # 1
            }
        ]
        returns a list of dictionaries
        """
#        nyarlathotep: list = [{},{}]
        kraken.insert(0, self.create_csv_writerow())
        for child in self.children.items():
            if not isinstance(child[1], Node):
                raise TypeError('Child is not an instance of', Node)
            child[1].create_csv_writerows(kraken)
        #! dict needs to be reorganized to be in the correct order base for output
        if not len(kraken) // 2 == 0:

            return kraken[::-1]
        else:
            return kraken


class NodeTree():
    """
    randomly generated tree for unit testing, adding class definition to main script instead of
    unit test module for better organization
    """
    headnode: Node
    population: int = 0

    def __traversetohead(self, node: Node) -> Node:
        """
        traverse the tree to the head node
        """
        while node.parent is not None:
            node = node.parent
        return node

    def __isnameunique(self, name: str, node: Node) -> bool:
        """
        check if any nodes in the tree have the same name as the name argument

        Args:
            name (str): ingredient name to check
            node (Node): node to check

        Returns:
            bool: returns true if the current node is the same as the name argument
        """
        if node.ingredient == name:
            return False
        else:
            for childnode in node.children.items():
                self.__isnameunique(name, childnode[1])
            return True

    def countleafs(self, leaf: Node, currentcount: int = 1) -> int:
        """
        counts how many leaf nodes were created in the tree

        Args:
            head (Node): node of a tree to count leaf nodes from
            currentcount (int, optional): how much nodes have been counted so far. Defaults to 1.

        Returns:
            int: how many leaf nodes were created in the tree
        """
        for cell in leaf.children.items():
            self.countleafs(cell[1], currentcount + 1)
        return currentcount

    def generateTree(self, population: int = random.randint(1, 10), canopynode: Node = Node(generatename(), None, 0, 1, 1, False, False)) -> Node:
        """
        generates a number of leaf nodes to create a tree of nodes

        Args:
            population (int, optional): the desired amount of nodes to generated.
            Defaults to random.randint(1,10).
            headnode (Node, optional): parent of randomly generated nodes.
            Defaults to Node(generatename()).

        Returns:
            Node: the headnode which contains all the randomly generated nodes
        """
        # check to see if the current population of the generated tree is less than the population
        # argument value
        if (self.countleafs(self.__traversetohead(canopynode))) < population:
            # generate a random name for the new node
            for _ in range(random.randint(1, population//2)):
                # create a new node with a random name, keep generating a new name until it is unique
                newnodename: str = generatename()
                while self.__isnameunique(newnodename, self.__traversetohead(canopynode)):
                    newnodename = generatename()
                # create a new node with the unique name and randomized amountmaderpecraft and amountneeded
                Node(newnodename, canopynode, 0, random.randint(
                    1, 100), random.randint(1, 100), False)
                # check once again if the population is less than the population argument value
                if self.countleafs(self.__traversetohead(canopynode)) < population:
                    break
        # call method recurisvely to generate more child subnodes
        for leafnode in canopynode.children.items():
            self.generateTree(population, leafnode[1])
        return self.__traversetohead(canopynode)

    def __init__(self, population: int = random.randint(1, 10)) -> None:
        self.headnode: Node = self.generateTree(population)
        self.population = self.countleafs(self.headnode)

def findlocalendpoints(cur: Node, foundendpoints: dict) -> dict:
    """
    look for endpoints connected to the tree at this node
    after this method is finished running, please clear its utilized dictionaryy
    """
    if foundendpoints is None:
        myendpoints: dict = {}
    else:
        myendpoints: dict = foundendpoints
    if len(cur.children) > 0:
        for child in cur.children.items():
            if isinstance(child[1], Node):
                findlocalendpoints(child[1], myendpoints)
    else:
        myendpoints.update({cur.instancekey: cur})
    returndict: dict = myendpoints
    return returndict


def promptint() -> int:
    """
    prompt the user to input a returnable integer

    Returns:
        int: an integer that is used to set the amountneeded, amount on hand, and
        the amount made per craft for a Node instance
    """
    mynum: int = 0
    while True:
        myinput = input('')
        if not myinput.isdigit():
            print('you can only type in a positive integer')
        else:
            mynum = int(myinput)
            break
    return mynum


def recursivearithmetic(cur: Node) -> int:
    """
    figure out the amount resulted of the augment Node instance,
    math function used: D = (B/C)A + (B/C)(min(Dqueue))
    - If there is no values in the queue it will default to 0
    Returns:
        int: returns the amount resulted of augment Node instance
    """
    # check and set minimum resulted if queue is not empty
    tentativeinteger: int = sys.maxsize
    if len(cur.queueamountresulted) == 0:
        tentativeinteger = 0
    else:
        for myinteger in cur.queueamountresulted.items():
            if myinteger[1] < tentativeinteger:
                tentativeinteger = myinteger[1]
    red = (cur.amountofparentmadepercraft / cur.amountneeded)
    blue = (red*cur.amountonhand) + (red*tentativeinteger)
    blue = round(math.floor(blue))
    cur.amountresulted = blue
    # recursively call the method
    if cur.parent is not None:
        cur.parent.queueamountresulted.update(
            {cur.ingredient: cur.amountresulted})
        recursivearithmetic(cur.parent)
    return cur.amountresulted


def reversearithmetic(cur: Node, desiredamount: int = 0) -> int:
    """
    find how much of a material you will need get a particular amount of an item you want

    Args:
        cur (Node): stores information about an ingredient
        desiredamount (int, optional): what the amount resulted should be given the
        returned value of this method. Defaults to 0.

    Raises:
        TypeError: child is not an instance of Node

    Returns:
        int: the amount on hand of the current Node's item needed to get the desired amount
    """
    cur.amountresulted = desiredamount
    red: float = ((cur.amountofparentmadepercraft/cur.amountneeded)
                  ** -1)*cur.amountresulted
    green: float = round(math.ceil(red))
    cur.amountonhand = int(max(red, green))
    traceback: bool = green > red
    if traceback:  # go back through the higher up nodes and increase the amount on hand by 1
        temp: Node = cur
        while temp.parent is not None:
            temp = temp.parent
            temp.amountonhand += 1
    # continue method recursively
    if len(cur.children) > 0:
        for childnode in cur.children.items():
            if not isinstance(childnode[1], Node):
                raise TypeError('child is not an instance of', Node)
            reversearithmetic(childnode[1], cur.amountonhand)
    return cur.amountonhand
# todo create methods for searching and cloning Node instances utilized in the __main__ populate method


def createclone(node: Node) -> Node:
    """
    creates a clone of the argument Node instance to be utilized in the populate method

    Args:
        node (Node): stoes information about an ingredient, node to be cloned

    Returns:
        Node: returns a clone of the node with the same values except for the instancekey and the
        address pointer
    """
    # clone must have a differing pointer address and instancekey
    newnode: Node = Node(node.ingredient, None, node.amountonhand,
                         node.amountneeded, node.amountofparentmadepercraft, False, False)
    newnode.treekey = node.treekey
    for childnode in node.children.items():
        newchildnode: Node = Node(childnode[1].ingredient, newnode,  # pylint: disable=unused-variable
                                  childnode[1].amountonhand,
                                  childnode[1].amountneeded,
                                  childnode[1].amountmadepercraft, False, False)
    return newnode
# end def


def iscircularilylinked(node: Node) -> bool:
    """
    checks to see if there is a circularily linked connection in the nodes
    using the tortoise and the hare method
    Args:
        node (Node): stores information about an ingredient

    Returns:
        bool: returns true if there is a circularily linked connection
    """
    hare: Node = node  # ? faster pointer
    tortoise: Node = node  # ? slower pointer
    return hare is tortoise
# end def


def searchnodequery(ingredient: str) -> dict:
    """
    search through a dictionary of Nodes to find a Node with the same ingredient name

    Args:
        ingredient (str): the name of the ingredient to search for

    Raises:
        TypeError: the key is not an integer and the value is not an instance of Node

    Returns:
        dict: all nodes found to have the same ingredient name as the search parameter, will returns {-1: None} if no nodes are found to have the same ingredient name
    """

    # if no nodes were found, return {-1:None}, else return the found nodes in the dictionary
    foundqueries: dict = {}
    # type check that all the entries in the GLOBALNODEDICT are Node instances
    # key value pair (instancekey, : Node)
    for index, node in enumerate(GLOBALNODEDICT.items()):
        if not isinstance(node[1], Node) or not isinstance(node[0], int):
            raise TypeError('searching failure at index', index,
                            'of the global nodes dictionary')
    # check to see the ingredient is in any item[1] of the GLOBALNODEDICT
    for node in GLOBALNODEDICT.items():
        # if the ingredient is found in the node, add it to the foundqueries dictionary
        if node[1].ingredient == ingredient:
            foundqueries.update({node[0]: node[1]})
    if len(foundqueries) == 0:
        return {-1: None}
    return foundqueries


def tentative_method_1_issue1(ingredient: str, parent: Node, promptamounts: bool = False) -> Node:
    """
    submethod for the populate method, only run this method for creating a new node if the search
    query does not return a dictionary of {-1:None}

    Args:
        ingredient (str): name of the ingredient
        parent (Node): parent instance of the node to be created
        promptamounts (bool, optional): boolean to determine if the constructor of the Node should prompt the input amounts method. Defaults to False.

    Raises:
        TypeError: search query failed because of invalid values in the search dictionary

    Returns:
        Node: created subnode
    """
    foundnodes: dict = searchnodequery(ingredient)
    # ! search did not find the ingredient in the global dictionary
    if foundnodes == {-1: None}:
        return Node(ingredient, parent, 0, 1, 1, promptamounts)
    else:
        displaylist: list = []
        print("What do you want to copy any of these nodes (Type in any of the numbers, type in\
                  an invalid number to create a completely new node):")
        # for all the found choices, reorganize the found choices into a list of tuples
        for index, node in enumerate(foundnodes.items()):
            # make sure you type check the dictionary
            if not isinstance(node[1], Node) or not isinstance(node[0], int):
                raise TypeError('searching failure at index',
                                index, 'of the global nodes dictionary')
            # create a list of tuples
            if node not in displaylist:
                displaylist.append({index: node})
        # display the list of tuples
        for index, node in enumerate(displaylist):
            print(displaylist[index], end='. ')
            print(displaylist[index][1].ingredient, end=' ')
            # if the node has children, display the first three children of the node at the current
            # index of the list of tuples
            if len(displaylist[index][1].children) > 0:
                print("children:", end=' ')
                for child in displaylist[index][1].children.items():
                    print(child[1].ingredient, end=', ')
            print('')
        # get the user input
        while True:
            mymethodinput: str = input()  # todo find a better name for this variable
            if not mymethodinput.isdigit():
                print('Invalid input, please enter a number between',
                      1, 'and', len(displaylist))
            # check if the input from the user is a valid number between 1 and the length of the
            # list
            elif mymethodinput.isdigit() and int(mymethodinput) > 0 and int(mymethodinput) <= len(displaylist):
                # create a clone of the node at the index position - 1 of the list of tuples
                return createclone(displaylist[int(mymethodinput) - 1][1])
            else:
                # create a regular node
                return tentative_method_1_issue1(generatename()+generatename()+generatename(), parent, promptamounts)


def populate(cur: Node):
    """
    creates new child instances during script runtime

    Args:
        cur (Node): parent instance, creates children instances for this node

    Raises:
        TypeError: this method continues recursively, if the child is not an instance
        of the same class as the augment, this is unintended behavior and will raise an error
        to catch it
    """
    inputqueue: dict = {}
    checkstring: str = cur.ingredient
    # output ingredient trail
    if cur.parent is not None:
        tempinstance: Node = cur
        print('TRAIL: ', end='')
        while True:
            if tempinstance.parent is not None:
                print(tempinstance.ingredient, '-> ', end='')
                tempinstance = tempinstance.parent
            else:
                print(tempinstance.ingredient)
                break
        checkstring = tempinstance.ingredient
    # prompt user to input ingredients
    print('What ingredients do you need to create', cur.ingredient, end=':\n')
    while True:
        myinput = input('')
        myinput = myinput.strip()
        # input validation
        duplicated: bool = False
        if len(inputqueue) > 0:
            for word in inputqueue.items():
                duplicated = word[1] == checkstring
                if duplicated:
                    break
        if duplicated:
            print('You already typed that in')
        elif myinput == checkstring:
            print('Invalid input, we are trying to make that item!')
        elif myinput == cur.ingredient:
            print('You cannot type that in')
        elif len(myinput) == 0:
            break
        else:
            inputqueue.update({len(inputqueue): myinput})
    # create new child instances
    tempbool: bool = True
    for newnodename in inputqueue.items():
        # if search method doesn't return a dictionary with a key of -1 and a value of None
        # prompt for copy
        # else
        # create new node
        # prompt if the user wants to copy an existing node if the search query returns a dictionary
        # that deosn't have a key of -1 and a value of None
        # todo have someone test out the code
        _ = tentative_method_1_issue1(newnodename[1], cur, tempbool)
        tempbool = False
#!        searchquery: dict = searchnodequery(newnodename[1])
#!        if searchquery == {-1: None}:
#!            Node(newnodename[1], cur, 0, 1, 1, tempbool)
#!        else: #! search did not return {-1: None}
#!            print("What do you want to copy any of these nodes (Type in any of the numbers, type in\
#!                  an invalid number to create a completely new node):")
        # create a dictionary of the found nodes, and print them out
        # if the user doesn't input a valid number choice for any node they want to copy,
        # assume default behavior, the else branch of this for-loop
    # input current argument node into the global dictionary
    GLOBALNODEDICT.update({cur.instancekey: cur})
    # continue method runtime
    for child in cur.children.items():
        if isinstance(child[1], Node):
            populate(child[1])
        else:
            raise TypeError('child is not an instance of', Node)


def printprompt():
    """
    prints out introduction to program, prompts the user which Mode they want to utilize
    """
    print('Which mode do you want to use:')
    print('Mode A - You are trying to figure out how much of your desired item you can make with the current supply of materials (Type in A)')  # pylint:disable=C0301
    print('Mode B - You are trying to figure out how much base materials you need to create a certain amount of your desired item, (Type in B)')  # pylint:disable=C0301
    print("Type in 'H' if you need a reminder of the prompt\n")


def reformat_output(endpoints: dict):
    """reformat the output to be more readable

    Args:
        endpoints (dict): dictionary of all the endpoints from a given Node instance tree
    """
    # set the new dictionary to be empty
    red_dict: dict = {}
    # set the new dictionary to have unique ingredients as keys and a list of tuples of the parent
    # of said endpoint instance and the amount on hand as values
    for node in endpoints.items():
        if node[1].ingredient not in red_dict:
            red_dict.update(
                {node[1].ingredient: [(node[1].parent.ingredient, node[1].amountonhand)]})
        else:
            red_dict[node[1].ingredient].append(
                (node[1].parent.ingredient, node[1].amountonhand))

    output_dictionary: dict = {}
    for item in red_dict.items():
        orangeinteger: int = 0  # sum of the amount on hand of each tuple element
        for orangenumber in item[1]:
            orangeinteger += orangenumber[1]
        for orangetuple in item[1]:
            if item[0] not in output_dictionary:
                output_dictionary.update({item[0]: [str(round(
                    (orangetuple[1]/orangeinteger)*100, 2))+'% ('+str(orangetuple[1])+'x) used in '+orangetuple[0]]})  # pylint:disable=C0301
            else:  # if item is in the outputdictionary, append the string to the list
                output_dictionary[item[0]].append(
                    str(round((orangetuple[1]/orangeinteger)*100, 2))+'% ('+str(orangetuple[1])+'x) used in '+orangetuple[0])  # pylint:disable=C0301
    # output the dictionary keys and values
    for item in output_dictionary.items():
        print(item[0], end=' (')
        for index, string in enumerate(item[1]):
            if index == len(item[1])-1:
                print(string, end='')
            else:
                print(string, end=', ')
        print(')')

# create a method that writes to the .csv file

# todo find a new name for this method


def tentative_method_issue3(ghatanothoa: Node):
    """
    method that writes to the .csv file

    Args:
        ghatanothoa (Node): stores information about the an ingredient
    """
    #!outputcsvlines: dict = ghatanothoa.create_csv_writerow()
    # open the .csv file in write mode
    with open(CSVFILENAME, 'a', encoding='UTF-8', newline='') as csvfile:
        # write the field names onto the file
        field_names = [
            'Tree_Key',  # 74nry8keki
            'Ingredient',  # Coal
            'Ingredient_Alias',  # Coal_[UNIQUE_ID APPENDED]
            # ? if the ingredient name is not unique, append a unique string to the end of the
            # ? ingredient name
            'Parent_of_Ingredient',  # Carbon
            'Amount_on_Hand',  # 0
            'Amount_Made_Per_Craft',  # 1
            'Amount_Needed_Per_Craft',  # 10
            'Generation'  # 1
        ]
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        # write the data onto the file
        writer.writerows(ghatanothoa.create_csv_writerows([]))
        csvfile.close()
    print('Successfully wrote to the .csv file called', CSVFILENAME)
# end def
# todo find a new name for this method


def tentative_method_2_issue3() -> bool:
    """
    check if the an exact copy of the ingredient tree already exists in the .csv file

    Args:
        zvilpogghua (Node): stores information about the an ingredient, head node of the increase tree

    Returns:
        bool: True if the an exact copy of the ingredient tree already exists in the .csv file, False otherwise
    """
    # check if the augment is the head node, if not, traverse upward to the head node
    # open the .csv file in read mode (mode='r')
    # parse the tree for the head node instances
    foundheadnodes: dict = {}  # pylint:disable=unused-variable
    with open(CSVFILENAME, 'r', encoding='UTF-8', newline='') as csvfile:
        # create a csv reader object
        reader = csv.DictReader(csvfile)  # pylint:disable=unused-variable
        # iterate over each row in the csv file and check if the row is a head node
    #! call method here
        csvnode: Node = Node()  # todo remove this line when finishing this method
        # todo remove this line when finishing this method
        tentative_method_3_issue3(csvnode)
        # close the .csv file
        csvfile.close()
    # return True if the an exact copy of the ingredient already exists in the .csv file, False otherwise
    return False
#! potential unintended behavior, if the user inputs an ingredient name with the same name, the alias name will not be the same and the program will not detect an exact copy of the tree
# end def


# todo find a new name for this method

def tentative_method_3_issue3(csvnode: Node):
    """
    creates a tree from a head node in the .csv file once its detected,
    recursively links children nodes to their parent nodes

    Args:
        None
    """
    # open the .csv file in read mode (mode='r')
    # read the .csv file
    # close the .csv file
    # create a head node
    # recursively link children nodes to their parent nodes
    # return the head node
    return None
# end def


# todo find a new name for this method
def tentative_method_4_issue3() -> dict:
    """
    method that reads the contents of the .csv file

    Args:
        nightguant (Node): stores information about the an ingredient
    """
    # check if the .csv file exists in the current directory
    csvheadnodes: dict = {}
    if os.path.exists(CSVFILENAME):
        #  if it does, read the contents of the file
        with open(CSVFILENAME, 'r', encoding='UTF-8', newline='') as csvfile:
            # create a csv reader object
            reader = csv.DictReader(csvfile)
            # iterate over each row in the csv file and check if the row is a head node
            for row in reader:
                for item in row.items():
                    iscsvheadnode: bool = item[0] == 'Generation' and item[1] == '0'
                    if iscsvheadnode:
                        # if true, update the dictionary with the tree key and a head node instance
                        csvheadnodes.update(
                            {row['Tree_Key']: Node(row['Ingredient'], None, 0, 1, 1)})
                        # int (row['Amount_Made_Per_Craft'])
                        # int (row['Amount_on_Hand'])
                        # int (row['Amount_Needed_Per_Craft']),
                        # int (row['Generation'])
    # parse through the file and create a dictionary of head nodes
        csvfile.close()  # close the .csv file
        return csvheadnodes
    else:
        return {-1: None}
    # prompt the user to select a head node to utilize in the current mode of the program
# end def


def tentative_method_5_issue5(nightguant: Node):
    """
    prompt if the user wants input the ingredient tree into a .csv file
    if the user wants to input the ingredient tree into a .csv file, call the method that writes to
    the .csv file

    Args:
        nightguant (Node): stores information about the an ingredient
    """
    # prompt if the user wants input the ingredient tree into a .csv file
    print("Do you want to save this ingredient tree into the .csv file for future use?\
         ('Y' or 'N')")
    while True:
        tentative_string_name1: str = input()
        tentative_string_name1 = tentative_string_name1.strip()
        tentative_string_name1 = tentative_string_name1.upper()
        if tentative_string_name1 not in ('Y', 'N'):
            print('that input is not valid, please type in something else')
        elif len(tentative_string_name1) > 1:
            print('the length of the input is too long, please type in something else')
        # ! must be false, if returns true it means that the tree was already inputted onto the csv file
        elif tentative_string_name1 == 'Y' and not tentative_method_2_issue3():
            # call method that writes to the .csv file
            tentative_method_issue3(nightguant)
            break
        # ! must be true, if returns false it means that the tree was not already inputted onto the csv file
        elif tentative_string_name1 == 'Y' and tentative_method_2_issue3():
            print('the tree was already inputted onto the .csv file')
            break
        elif tentative_string_name1 == 'N':
            # do nothing
            break
        else:
            raise ValueError(
                'something went wrong,unknown boolean condition met')
# end def


if __name__ == '__main__':
    print('Welcome to Process Map (Python) v2.0!\n')
    while True:
        # prompt user which mode they want to run the program in
        printprompt()
        while True:
            userinput = (input(''))
            userinput = userinput.strip()
            userinput = userinput.upper()
            if userinput not in ('A', 'B', 'H'):
                print("That input is not valid, please type in 'A' or 'B'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one character')
            elif userinput == 'B':
                PROGRAMMODETYPE = 1
                # todo if the .csv file exists in the current directionary, ask the user if they want to use an of the ingredient trees in the file for the current program mode
                nodesfromcsv: dict = tentative_method_4_issue3()
                print("Do you want to chose any of these ingredient trees to modify from the .csv file?\
                      ('Y' or 'N')")
                if nodesfromcsv != {-1:None}:
                    for index,item in enumerate(nodesfromcsv.items()):
                        print(f'{index+1}. {item[1].ingredient}')
                break
            elif userinput == 'H':
                printprompt()
            else:
                PROGRAMMODETYPE=0
                # todo if the .csv file exists in the current directionary, ask the user if they want to use an of the ingredient trees in the file for the current program mode
#!                nodesfromcsv : dict = tentative_method_4_issue3()
#!                print("Do you want to chose any of these ingredient trees to modify from the .csv file?\
#!                      ('Y' or 'N')")
#!                if nodesfromcsv != {-1:None}:
#!                    for index,item in enumerate(nodesfromcsv.items()):
#!                        print(f'{index+1}. {item[1].ingredient}')
                break
        # prompt user to type in the name of the item they want to create
        while True:
            itemname=input(
                'What is the name of the item you want to create: ')
            itemname=itemname.strip()
            if len(itemname) == 0:
                print('You must type something in')
            else:
                break
        head=Node(itemname, None)
        if PROGRAMMODETYPE == 0:  # ? normal program mode
            populate(head)
            for subnode in findlocalendpoints(head, {}).items():
                recursivearithmetic(subnode[1])
            print('# resulted of', head.ingredient, '',
                  end=str(head.amountresulted)+'\n')
        else:  # ? Mode B
            print('How much', head.ingredient, 'do you want to create:')
            desirednumber: int=promptint()
            populate(head)
            reversearithmetic(head, desirednumber)
            # output the results
            print('To get', str(str(desirednumber)+'x'),
                  head.ingredient, 'you need the following:')
            results: dict=findlocalendpoints(head, {})
            # iterate through the dictionary and output the amounts on hand
            reformat_output(results)
        # prompt user if they want to output the results to a .csv file
        # todo insert prompt for outputting to .csv file
        tentative_method_5_issue5(head)
        # prompt the user to see if they want to input another tree
        print("\nDo you want to run the program again with another item tree?\
             ('Y' or 'N')")
        print("type in 'H' if you need to be reminded of the prompt")
        while True:
            userinput=(input(''))
            userinput=userinput.strip()
            userinput=userinput.upper()
            if userinput not in ('Y', 'N', 'H'):
                print("That input is not valid, please type in\
                     ('Y' or 'N')")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one character')
            elif userinput == 'N' or userinput == 'Y':
                break
        head.clearamountresulted()
        if userinput == 'N':
            break
    # terminate the program
    print('terminating process in 10 seconds')
    # close program in 10 seconds
    NANI=10
    while NANI > 0:
        time.sleep(1)
        NANI -= 1
