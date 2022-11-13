# pylint:disable=C0302
"""
Reformat of main.py
Changes:
- Added Enum for program Modes
- Added and fixed Search/Copy Node functionality
- Added ability to write ingredient trees to a CSV
- Added ability to read ingredient trees from a CSV
"""

import math
import os
import random
import sys
import time
from enum import Enum

import pandas


class ProgramState(Enum):
    """
    Enum for which mode the user selected during runtime
    """
    MODE_A = 0  # recursive arithmetic (amountresulted)
    MODE_B = 1  # inverse recursive arithmetic (amountonhand)


FILENAME: str = 'ingredient_trees.csv'
FIELDNAMES: list = [
    'Tree_Key',  # 74nry8keki',
    'Ingredient',  # Copper Wire
    'Ingredient_Alias',  # Copper_Wire2
    'Parent_of_Ingredient',  # Silicon Board
    'Amount_on_Hand',  # 0
    'Amount_Of_Parent_Made_Per_Craft',  # 9
    'Amount_Needed_Per_Craft',  # 0
    'Generation'  # 1
]


def promptint() -> int:
    """
    prompts the user for an postive integer and returns it

    Returns:
        int: postive integer from user input
    """
    while True:
        myinput = input('').strip()
        if not myinput.isdigit():
            print('you can only type in a positive integer')
        elif int(myinput) < 0:
            print('please type in a postive integer')
        else:
            return int(myinput)


class NodeB:  # pylint: disable=R0903
    """
    a superclass of the Node class used to contain basic information about an ingredient
    """
    ingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}
    aliasingredient: str = ''

    def __init__(self, ingredient: str = '',
                 amountonhand: int = 0,
                 amountparentmadepercraft: int = 1,
                 amountneeded: int = 1) -> None:
        """
        a superclass of the Node class used to contain basic information about an ingredient

        Args:
            ingredient (str, optional): name of the item stored. Defaults to ''.
            amountonhand (int, optional): how much of the ingredient you have to craft the direct
            parent item above it. Defaults to 0.
            amountparentmadepercraft (int, optional): how much of the parent ingredient is made with
            this ingredient. Defaults to 1.
            amountneeded (int, optional): amount of ingredient needed to craft the parent igredient
            once. Defaults to 1.
        """
        self.amountonhand = amountonhand
        self.amountparentmadepercraft = amountparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.amountresulted = 0
        self.aliasingredient = ingredient.replace(' ', '_')


class Node(NodeB):  # pylint: disable=R0913 #pylint: disable=R0902
    """
    primary class of the Node, used to stored information about an ingredient as well as
    information to identify the ingredient and its parent
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    treekey: str = ''
    isfromcsvfile: bool = False
    population: int = 1

    def __init__(self, ingredient: str = '',  # pylint: disable=R0913
                 parent=None,
                 amountonhand: int = 0,
                 amountparentmadepercraft: int = 1,
                 amountneeded: int = 1,
                 promptamountparentmade: bool = False,
                 promptamountsOn: bool = True,
                 isfromcsvfile: bool = False,
                 treekey: str = '') -> None:
        """
        primary class of the Node, used to stored information about an ingredient as well as
        information to identify the ingredient and its parent

        Args:
            ingredient (str, optional): name of the item stored. Defaults to ''.
            amountonhand (int, optional): how much of the ingredient you have to craft the direct
            parent item above it. Defaults to 0.
            amountparentmadepercraft (int, optional): how much of the parent ingredient is made with
            this ingredient. Defaults to 1.
            amountneeded (int, optional): amount of ingredient needed to craft the parent igredient
            once. Defaults to 1.
            promptamountparentmade (bool, optional): determines if the program should prompt user to
            type in a number for the amount of the parent ingredient made per craft.
            Defaults to False.
            isfromcsvfile (bool, optional): a boolean to track if the created Node instance is from
            the CSV file. Defaults to False.
            treekey (str, optional): a string of about 10 to 20 alphanumeric characters to help make
            each ingredient tree unique when written to a CSV file. Defaults to ''.
        """
        super().__init__(ingredient,
                         amountonhand,
                         amountparentmadepercraft,
                         amountneeded)
        self.treekey = treekey
        self.isfromcsvfile = isfromcsvfile
        self.instancekey = Node.instances
        self.children = {}
        self.parent = parent
        if self.parent is not None:
            self.generation = self.parent.generation + 1
            self.parent.children.update({self.instancekey: self})
            self.treekey = self.parent.treekey
        else:
            self.generation = 0
            if isfromcsvfile:
                self.treekey = treekey
            else:
                self.treekey = self.gen_treekey()
        if promptamountsOn and __name__ == '__main__':
            self.__inputnumerics(promptamountparentmade)
        self.updatepopulation()
        Node.instances += 1

    def __inputnumerics(self, promptamountparentmade: bool):
        """
        prompt input of the numeric data for the instance from the user
        """
        # $ only in MODE A - prompt amountonhand
        while MODE == ProgramState.MODE_A:
            print('How much', self.ingredient, 'do you have on hand: ')
            self.amountonhand = promptint()
            if self.amountonhand < 0:
                print('That number is not valid')
            else:
                break
        if self.parent is not None:
            # $ only if older sibiling has not been prompted, prompt amountmadepercraft
            while promptamountparentmade:  # ? should this be prompted depending on if it was cloned
                print('How much', self.parent.ingredient,
                      'do you create each time you craft it: ')
                self.amountparentmadepercraft = promptint()
                if self.amountparentmadepercraft < 1:
                    print('That number is not valid')
                else:
                    promptamountparentmade = False
                    break
            # $ prompt amountneeded
            while True:
                print('How much', self.ingredient, 'do you need to craft',
                      self.parent.ingredient, '1 time: ')
                self.amountneeded = promptint()
                if self.amountneeded < 1:
                    print('That number is not valid')
                else:
                    break

    @classmethod
    def gen_treekey(cls, maxlength: int = random.randint(10, 20)) -> str:
        """
        generate a unique tree key of random alphumeric characters
        """
        cls.treekey = ''
        for _ in range(0, maxlength):
            cls.treekey += random.choice(
                '0123456789abcdefghijklmnopqrstuvwxyz')
        return cls.treekey

    def recursivearithmetic(self) -> int:
        """
        tentative docstring description
        """
        # check and set minimum resulted if queue is not empty
        tentativeinteger: int = sys.maxsize
        if len(self.queueamountresulted) == 0:
            tentativeinteger = 0
        else:
            for myinteger in self.queueamountresulted.items():
                if myinteger[1] < tentativeinteger:
                    tentativeinteger = myinteger[1]
        red = (self.amountparentmadepercraft / self.amountneeded)
        blue = (red*self.amountonhand) + (red*tentativeinteger)
        blue = round(math.floor(blue))
        self.amountresulted = blue
        # recursively call the method
        if self.parent is not None:
            self.parent.queueamountresulted.update(
                {self.ingredient: self.amountresulted})
            self.parent.recursivearithmetic()
        return self.amountresulted

    def reversearithmetic(self, desiredamount: int = 0) -> int:
        """
        tentative docstring description
        """
        self.amountresulted = desiredamount
        red: float = ((self.amountparentmadepercraft/self.amountneeded)
                      ** -1)*self.amountresulted
        green: float = round(math.ceil(red))
        self.amountonhand = int(max(red, green))
        traceback: bool = green > red
        if traceback:  # traverse upward and increase the amount on hand by 1
            temp: Node = self
            while temp.parent is not None:
                temp = temp.parent
                temp.amountonhand += 1
        # continue method recursively
        if len(self.children) > 0:
            for childnode in self.children.items():
                if not isinstance(childnode[1], Node):
                    raise TypeError('child is not an instance of', Node)
                childnode[1].reversearithmetic(self.amountonhand)
        return self.amountonhand

    def modifytreekey(self, newtreekey: str):
        """
        change the tree key of the node and all of its children
        """
        self.treekey = newtreekey
        for subnode in self.children.items():
            subnode[1].modifytreekey(newtreekey)

    def pandasrow(self) -> dict:
        """
        create a row of data of the Node for writing to the csv file

        Returns:
            dict: a dict of information about the Node
        """
        pandas_row: dict = {}
        pandas_row.update({'Tree_Key': self.treekey})
        pandas_row.update({'Ingredient': self.ingredient})
        pandas_row.update({'Ingredient_Alias': self.aliasingredient})
        if self.parent is not None:
            pandas_row.update(
                {'Parent_of_Ingredient': self.parent.ingredient})
        else:
            pandas_row.update({'Parent_of_Ingredient': 'None'})
        pandas_row.update({'Amount_on_Hand': str(self.amountonhand)})
        pandas_row.update(
            {'Amount_Made_Per_Craft': str(self.amountparentmadepercraft)})
        pandas_row.update(
            {'Amount_Needed_Per_Craft': str(self.amountneeded)})
        pandas_row.update({'Generation': str(self.generation)})
        return pandas_row

    def pandastree_row(self, rows: list) -> list:
        """
        return a list of all the pandas rows in the tree

        Args:
            rows (list): a list of pandas rows (dicts of data)

        Returns:
            list: a list of dicts containing the data for each node to be written onto a csv file
        """
        rows.append(self.pandasrow())
        for child in self.children.items():
            child[1].pandastree_row(rows)
        return rows

    def updatepopulation(self, population: int = 0):
        """
        sets and updates the population attribute of the Node accordingly
        """
        self.population = population
        for subnode in self.children.items():
            subnode[1].updatepopulation(population)

    def findendpoints(self, endpoints: dict) -> dict:
        """
        returns a dictionary of nodes with no children

        Args:
            endpoints (dict): _description_

        Returns:
            _type_: _description_
        """
        for subnode in self.children.items():
            if len(subnode[1].children) == 0:
                endpoints.update({subnode[1].instancekey: subnode[1]})
            else:
                subnode[1].findendpoints(endpoints)
        return endpoints

    def reformat_output(self):  # pylint:disable=R0912
        """
        condenses the output of the tree into a more readable format with percentages
        """
        # ! this method can only run when there is are more than one nodes in the ingredient tree,
        # ! otherwise it will crash
        # set the new dictionary to be empty
        temp = self
        if not isinstance(temp, Node):
            raise TypeError('temp is not an instance of', Node)
        while temp.parent is not None:
            temp = temp.parent
        compressedendpoints: dict = {}
        # set the new dictionary to have unique ingredients as keys
        # and a list of tuples of the parent of said endpoint instance and the
        # amount on hand as values
        for node in temp.findendpoints({}).items():
            if node[1].ingredient not in compressedendpoints:
                compressedendpoints.update(
                    {node[1].ingredient: [(node[1].parent.ingredient,
                                           node[1].amountonhand)]})
            else:
                compressedendpoints[node[1].ingredient].append(
                    (node[1].parent.ingredient,
                     node[1].amountonhand))
        output_dictionary: dict = {}
        for item_a in compressedendpoints.items():
            orangeinteger: int = 0  # sum of the amount on hand all tuple items
            for orangenumber in item_a[1]:
                orangeinteger += orangenumber[1]
            for orangetuple in item_a[1]:
                if item_a[0] not in output_dictionary:
                    output_dictionary.update({item_a[0]: [str(round(
                        (orangetuple[1]/orangeinteger)*100, 2)) +
                        '% ('+str(orangetuple[1])+'x) used in ' +
                        orangetuple[0]]})
                else:  # if item is in the dict, append the string to list
                    output_dictionary[item_a[0]].append(
                        str(round((orangetuple[1]/orangeinteger)*100, 2)) +
                        '% ('+str(orangetuple[1])+'x) used in ' +
                        orangetuple[0])
        # output the dictionary keys and values
        for item_a in output_dictionary.items():
            print(item_a[0], end=' (')
            for index, string in enumerate(item_a[1]):
                if index == len(item_a[1])-1:
                    print(string, end='')
                else:
                    print(string, end=', ')
            print(')')


def nodecount(node: Node) -> int:
    """
    counts how many nodes are in the connected ingredient tree

    Returns:
        int: the number of nodes in the tree (based on the size of list of nodes)
    """
    return len(head(node).pandastree_row([]))


def makealiasunique(node: Node):
    """
    makes all the ingredient aliases in the ingredient tree unique

    Args:
        node (Node): current node
    """
    # make all nodes in the tree have unique ingredient aliases
    # get a list of all the nodes in the ingredient tree with the same ingredient alias
    # as the passed node instance
    nodesaliases: list = allaliases(node, node.aliasingredient, [])
    # if the list is greater than 1, then parse through the list to make each alias unique
    if len(nodesaliases) > 1:
        # make uniue by appending the index to the alias
        for redindex, reditem in enumerate(nodesaliases):
            for blueindex, blueitem in enumerate(nodesaliases):
                if redindex != blueindex and reditem.aliasingredient == blueitem.aliasingredient:
                    blueitem.aliasingredient += str(blueindex)
    # recrusively call the function on each child node
    for subnode in node.children.items():
        makealiasunique(subnode[1])


def allaliases(node: Node, alias: str, aliases: list) -> list:
    """
    returns a list of all the nodes with the same alias

    Args:
        node (Node): node to check if it has the same ingredient alias value
        alias (str): nickname of Node instance
        aliases (list): list of nodes with the same alias to search for

    Returns:
        list: a list of Nodes containining the same ingredient alias
    """
    if node.aliasingredient == alias:
        aliases.append(node)
    # recrusively search for nodes that have the same ingreident alias as the passed alias
    for subnode in node.children.items():
        allaliases(subnode[1], alias, aliases)
    return aliases


def writetreetocsv(headnode: Node):
    """
    writes an ingredient tree onto a csv file

    Args:
        headnode (Node): the head node of the ingredient tree
    """
    # check if the csv file exists
    # if the file is not in the directory, create it
    if not os.path.exists(FILENAME):
        # create the file
        pandas.DataFrame(columns=FIELDNAMES).to_csv(
            FILENAME, index=False)
        # open file again to append to it
        writetreetocsv(headnode)
    else:
        # then write to the file but calling the method again recursively
        for row in headnode.pandastree_row([]):
            pandas.DataFrame(row, index=[0]).to_csv(
                FILENAME, mode='a', header=False, index=False)


def promptheadname() -> str:
    """
    prompts the user for the head node name

    Returns:
        str: the name of the head node
    """
    while True:
        myinput: str = input('What is the name of the item you are trying to make: ').strip()  # noqa: E501 #pylint: disable=line-too-long
        if len(myinput) == 0:
            print('Your input cannot be empty!')
        else:
            return myinput


def head(node: Node) -> Node:
    """
    traverse to the parent most Node

    Args:
        node (Node): starting Node

    Returns:
        Node: parent most Node of the starting Node
    """
    while node.parent is not None:
        node = node.parent
    return node


def trail(node: Node):
    """
    print the ingredient trail leading up to the parent most Node

    Args:
        node (Node): starting Node
    """
    print('TRAIL: ', end='')
    while True:
        if node.parent is not None:
            print(node.ingredient, '-> ', end='')
            node = node.parent
        else:
            print(node.ingredient)
            break


def outputingredients(node: Node):
    """
    populate submethod, print the subingredients of the parameter Node

    Args:
        node (Node): parent node, the node to print the subingredients of
    """
    subingredients: list = []
    for subnode in node.children.items():
        subingredients.append(subnode[1].ingredient)
    print('+ These ingredients are already in the tree:\n')
    # output the ingredients
    for index, ingredient in enumerate(subingredients):
        print(f'{index+1}. {ingredient}')
    print('')


def parsecsv() -> dict:
    """
    parses the csv file to look for head nodes, returns a dictionary of them

    Returns:
        dict: dictionary of head node instances from the csv file, key is the treekey
        and the value is the head node instance
    """
    headnodes: dict = {}
    # if there are no head nodes,
    # or the file does not exist return {-1: None}
    if not os.path.exists(FILENAME):
        return {-1: None}
    # parse csv for head nodes
    for purple in pandas.read_csv(FILENAME).to_dict('index').items():
        # convert the values of the dictionary to a list to see if it holds valid values
        green: list = list(purple[1].values())
        if green[3] == 'None' and green[5] == 1 and green[6] == 1 and green[7] == 0:
            headnodes.update({green[0]: Node(ingredient=green[1],
                                            parent=None,
                                            promptamountparentmade=False,  # noqa: E501 #pylint: disable=line-too-long
                                            treekey=green[0],
                                            isfromcsvfile=True,
                                            promptamountsOn=False)})
    if len(headnodes) == 0:
        return {-1: None}
    return headnodes


def createtree(node: Node, pandasrow: list) -> bool:
    """
    figure out where to emplace the Node in the tree

    Args:
        node (Node): parent of Node to be emplaced
        pandasrow (list): row of data from the CSV file

    Raises:
        TypeError: the row of data contains an invalid amount of values

    Returns:
        bool: was the node actually emplaced
    """
    if len(pandasrow) != len(FIELDNAMES):
        raise TypeError('The row of data is not the correct length')
    # remove any underscores from the ingredient
    pandasrow[1] = pandasrow[1].replace('_', ' ')
    # remove any underscores from the parent of the ingredient
    pandasrow[3] = pandasrow[3].replace('_', ' ')
    foundemplacelocation: bool = node.treekey == pandasrow[0] and pandasrow[
        3] != 'None' and pandasrow[3] == node.ingredient and pandasrow[7] > 0 and node is not None and pandasrow[7] == node.generation + 1  # noqa: E501 #pylint: disable=line-too-long
    if foundemplacelocation:
        Node(pandasrow[1],
             parent=node,
             amountneeded=pandasrow[6],
             amountparentmadepercraft=pandasrow[5],
             amountonhand=pandasrow[4],
             treekey=pandasrow[0],
             # isfromcsvfile=True,
             promptamountsOn=False)
        red: str = '\x1B[31m' + node.ingredient + \
            '\x1B[0m'  # parent ingredient name
        blue: str = '\x1B[36m' + pandasrow[1] + '\x1B[0m'  # ingredient name
        print('emplaced node', red + ' | ' + blue)
        return True
    for subnode in node.children.items():
        createtree(subnode[1], pandasrow)
    return False


def createtreefromcsv(parent: Node) -> Node:
    """
    figures out where to create and link a new node from the csv file

    Args:
        parent (Node): potential parent node to link new node to
        pandasrow (list): data from csv file, creates node from it

    Returns:
        Node: parent most node of the tree
    """
    # check if the row has the correct amount of elements
    # the node must match the following requirements to link:
    # parent ingredient must be the same as the parent ingredient
    # treekey must be the same & generation > 0
    sublist: list = []
    for purple in pandas.read_csv(FILENAME).to_dict('index').items():
        # convert the values of the dictionary to a list
        green: list = list(purple[1].values())
        # if the tree key of the row matches the head node's tree key
        if green[0] == parent.treekey and green[3] != 'None':
            # the sublist contains node only from the tree
            sublist.append(green)
    # figure out where to emplace the node
    # $ correctly finds all nodes with the same treekey from the csv file
    for row in sublist:
        createtree(parent, row)
        # print('row', index, 'of', len(sublist), 'rows')
    return head(parent)


def search(node: Node, ingredient: str, results: list) -> list:
    """
    recursively search through the tree to find nodes with the same
    ingredient

    Args:
        node (Node): parent node, parse through its children recursively to
        update the search results
        ingredient (str): the name of the item you are searching for
        results (list): nodes that have the same ingredient as the parameter

    Returns:
        list: a list of nodes that have the same ingredient as the parameter
    """
    # if node is a subnode and the ingredient matches, update the list
    if node.parent is not None and node.ingredient == ingredient:
        results.append(node)
    # recrusively keep searching for nodes
    for subnode in node.children.items():
        search(subnode[1], ingredient, results)
    return results


def shouldclonechildren(ingredient: str, subnodes: dict) -> bool:
    """
    check to see if the ingredient is within the subnodes of its siblings nodes of its emplace
    location

    Args:
        ingredient (str): name of item to check if it is in the subnodes
        subnodes (dict): a dictionary of subnodes of the parent node (emplace parent location)

    Raises:
        TypeError: dictionary does not contain int, node pairs
        TypeError: the parent of the subnodes are not the same

    Returns:
        bool: whether or not the ingredient is in the subnodes, used to help determine if the
        subnodes should be cloned
    """
    if len(subnodes) == 0:
        return True
    # convert subnodes dict to a list of nodes
    subnodeslist: list = []
    for subnode in subnodes.items():
        # dict must be have a key integer and a Node instance as the value
        if not isinstance(subnode[1], Node) and not isinstance(subnode[0], int):
            raise TypeError('subnodes is not a dictionary', Node, 'subnodes')
        # check of any node instance in the convert list does not have a the same parent
        # raise an error if the parent is not the same in all nodes
        subnodeslist.append(subnode[1])
        for redindex, rednode in enumerate(subnodeslist):
            for blueindex, bluenode in enumerate(subnodeslist):
                if redindex != blueindex and rednode.parent is not bluenode.parent:
                    raise TypeError('subnodes is not a dictionary',
                                    Node, 'subnodes with the same parent')
    # create a list of ingredient names that are within all the nodes in the dict
    subingredientnames: list = []
    for subnode in subnodeslist:
        for childnode in subnode.children.items():
            subingredientnames.append(childnode[1].ingredient)
    # check if the ingredient is in the list of subingredient names
    if ingredient in subingredientnames:
        return False
    return True


def clone(node: Node, clonechildren: bool = True) -> Node:
    """
    creates a returnable clone of the node passed into the method

    Args:
        node (Node): current node instance to copy and clone
        clonechildren (bool, optional): should the have its subnodes cloned aswell.
        Defaults to True.

    Returns:
        Node: a clone of a node
    """
    # (industrial battery GEN==1, input protocite)
    # if the parent ingredient is in the same generation as the clone,
    # do not clone the children, set the parent as its grandparent node

    # create a copy of the parameter node
    if not clonechildren:
        if node.parent is not None and node.parent.parent is not None and isinstance(node.parent.parent, Node):  # pylint:disable = line-too-long
            bluenode: Node = Node(ingredient=node.ingredient,
                                  parent=node.parent.parent,
                                  amountonhand=node.amountonhand,
                                  amountneeded=node.amountneeded,
                                  amountparentmadepercraft=node.amountparentmadepercraft,
                                  isfromcsvfile=node.isfromcsvfile,
                                  promptamountsOn=False)
            return bluenode
        # fallback incase grandparent is not valid
        # $ go back and examine this return branch more
        return clone(node, True)
    rednode: Node = Node(ingredient=node.ingredient,
                         parent=node.parent,
                         amountonhand=node.amountonhand,
                         amountneeded=node.amountneeded,
                         amountparentmadepercraft=node.amountparentmadepercraft,
                         isfromcsvfile=node.isfromcsvfile,
                         promptamountsOn=False)
    # create a copy of all the children of the parameter node
    for subnode in node.children.items():
        Node(ingredient=subnode[1].ingredient,
                parent=subnode,
                amountonhand=subnode[1].amountonhand,
                amountneeded=subnode[1].amountneeded,
                amountparentmadepercraft=subnode[1].amountparentmadepercraft,  # noqa: E501 #pylint: disable=line-too-long
                promptamountparentmade=False,
                isfromcsvfile=subnode[1].isfromcsvfile,
                promptamountsOn=False)
    return rednode


def subpopulate(node: Node, ingredient: str) -> Node:
    """
    create a subnode and link it to the parent node

    Args:
        node (Node): parent Node to link back to

    Returns:
        Node: new subnode to link back to the parent Node
    """
    # create a list of subnodes that have the same ingredient as the parameter
    parseresults: list = search(head(node), ingredient, [])
    # if the list is empty return a defaultly created new node Node
    for subnode in parseresults:
        if not isinstance(subnode, Node):
            raise TypeError('item in the list is not an instance of', Node)
    if len(parseresults) == 0:
        return Node(ingredient, node)
    # else, prompt the user to create a linkable clone of the new node
    print('+ amount of', ingredient,
          'on Hand (needed to make 1', head(node).ingredient, end=')\n')
    print('++ amount of the parent made per craft')
    print('+++ amount Needed to craft parent item once\n')
    if MODE == ProgramState.MODE_B:
        head(node).reversearithmetic(1)
    for index, subnode in enumerate(parseresults):
        # come back to this and see if do the math on the tree
        # will help differiate the values (industral battery)

        # output the choices of subnodes:
        # parent ingredient, amountneeded, amountmadepereachcraft
        print(index+1, end=str('. ' + subnode.parent.ingredient
                               + ' | + ' + str(subnode.amountonhand)
                               + ' | ++ ' + str(subnode.amountneeded)
                               + ' | +++ ' + str(subnode.amountparentmadepercraft)+'\n'))
    # todo make sure program doesn't crash when user's input is blank
    print('Choose which verison of', ingredient, 'to clone:')
    userchoice: int = promptint() - 1
    # if the user chooses to create a new node, return a clone subnode
    if userchoice < 0 or userchoice > len(parseresults)-1:
        # if the user did not input a valid index
        # if not return the defaultly created new node
        return Node(ingredient, node)
    # check if the ingredient is in any of the subnodes of its sibilings
    clonenode: Node = clone(
        parseresults[userchoice],  # node that will be cloned
        shouldclonechildren(ingredient, node.children))  # bool to determine to clone subnodes
    return clonenode


def populate(node: Node) -> Node:  # pylint: disable=R0912
    """
    create a tree of Nodes

    Args:
        node (Node): parent the subnodes will be linked to

    Returns:
        Node: the head of the ingredient tree
    """
    # update population attribute of Node
    node.updatepopulation(nodecount(node))
    # output the ingredient trail if there is a parent Node
    if node.parent is not None:
        trail(node)
    # prompt the user to ingredient tree
    userinputs: list = []  # list of tuples (string, bool)
    # append subnode ingredients to the list if there are any
    for subnode in node.children.items():
        userinputs.append((subnode[1].ingredient, True))
    # prompt the user for ingredients
    print('What ingredients do you have need to create',
          node.ingredient, end=':\n')
    # if there are subnodes, prompt the user to select from the list
    if len(node.children) > 0:
        outputingredients(node)
    while True:
        # create ingredients blacklist
        ingredientblacklist: list = []
        for ingredient in userinputs:
            ingredientblacklist.append(ingredient[0])
        # prompt the user for an ingredient
        myinput: str = input('').strip()
        # check to see if the user input is the same as the parent or head Node
        if myinput in [head(node).ingredient, node.ingredient]:
            print('Invalid input, we are trying to make that item!')
        # if the length of the user input is 0, break the loop
        elif myinput in ingredientblacklist:
            print('Invalid input, duplicate inputs!')
        # if the input is empty, break out of the loop
        elif len(myinput) == 0:
            break
        # append to the user inputs list if all the checks pass
        else:
            # if the condition is met, append the input to the list
            userinputs.append((myinput, False))
    # create subnodes for each ingredient using the subpopulate method
    for ingredient in userinputs:
        # if ingredient[1] is False, the ingredient is not already in the tree (from csv)
        if not ingredient[1]:
            # searchresults: list = search(head(node), ingredient[0], [])
            subpopulate(node, ingredient[0])
    # update population attribute of Node
    node.updatepopulation(nodecount(node))
    # recrusively continue to populate the tree
    for subnode in node.children.items():
        populate(subnode[1])
    # if the program Mode is A and the length of the children Nodes are 0
    if MODE == ProgramState.MODE_A and len(node.children) == 0:
        # call the arithmetic method
        node.recursivearithmetic()
    # return the head of the ingredient tree
    return head(node)


def superpopulate() -> Node:
    """
    creates an ingredient tree and returns its head node

    Returns:
        Node: head node of the populated ingredient tree
    """
    # check to see if there is a csv file in the current directory
    if not os.path.exists(FILENAME):
        # if the file exists, parse it for head nodes
        nodetree: Node = head(populate(Node(promptheadname())))
        nodetree.modifytreekey(nodetree.gen_treekey())
        return nodetree
    # parse the csv file for head nodes
    foundheadnodes: dict = parsecsv()
    # if there are no head nodes {-1:None}
    if foundheadnodes == {-1: None}:
        # return new ingredient tree
        nodetree: Node = head(populate(Node(promptheadname())))
        nodetree.modifytreekey(nodetree.gen_treekey())
        return nodetree
    userchoices: list = []
    # convert the dict into a list of node instances
    for node in foundheadnodes.items():
        userchoices.append(node[1])
    # sort the list of nodes by the amount of children
    for blue in range(0, len(userchoices)-1):
        for red in range(0, len(userchoices)-1):
            if not isinstance(userchoices[red], Node):
                raise TypeError('item in the list is not an instance of', Node)
            if head(userchoices[blue]).instancekey > head(userchoices[red]).instancekey:
                # flake8: noqa
                userchoices[blue], userchoices[red] = userchoices[red], userchoices[blue]
                # swap red and blue
    # output the choices
    print('Do you want to choose from one of the following trees as a preset?')
    for index, node in enumerate(userchoices, start=1):
        print(index, end=str('. ' + node.ingredient)+'\n')
    # prompt the user to make select a head node to modify
    print('Please choose a head node to modify, select a number out of range to create a new tree')
    userchoice: int = promptint()-1
    # if the user chosesn an index out or range, return a new tree
    if userchoice < 0 or userchoice > len(userchoices)-1:
        nodetree: Node = head(populate(Node(promptheadname())))
        nodetree.modifytreekey(nodetree.gen_treekey())
        return nodetree
    # return the head node of the chosen tree
    # create ingredient tree out of the csv file
    nodetree: Node = head(populate(createtreefromcsv(userchoices[userchoice])))
    nodetree.modifytreekey(nodetree.gen_treekey())
    return nodetree


if __name__ == '__main__':
    MODE: ProgramState = ProgramState.MODE_A
    # prompt program mode
    print('Welcome to Process Map (Python) v2.0!\n')
    # program runtime loop
    while True:
        print('Which mode do you want to use:')
        print('Mode A - You are trying to figure out how much of your desired'
              ' item you can make with the current supply of materials'
              ' (Type in A)')
        print('Mode B - You are trying to figure out how much base materials'
              ' you need to create a certain amount of your desired item, ('
              'Type in B)')
        print("Type in 'H' if you need a reminder of the prompt\n")
        # prompt user which mode they want to run the program in
        while True:
            userinput = input('').strip().upper()
            if userinput not in ('A', 'B', 'H'):
                print("That input is not valid, please type in 'A' or 'B'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      'character')
            elif userinput == 'B':
                MODE = ProgramState.MODE_B
                break
            elif userinput == 'H':
                # print prompt again
                print('Which mode do you want to use:')
                print('Mode A - You are trying to figure out how much of your'
                      ' desired item you can make with the current supply of'
                      ' materials (Type in A)')
                print('Mode B - You are trying to figure out how much base'
                      ' materials you need to create a certain amount of your'
                      ' desired item, (Type in B)')
                print("Type in 'H' if you need a reminder of the prompt\n")
            else:
                MODE = ProgramState.MODE_A
                break
        # populate the ingredient tree
        ingredienttree: Node = superpopulate()
        # if the programde mode is B
        if MODE == ProgramState.MODE_B:
            # prompt the user for how much an item they want to make
            print('How much of the item do you want to make?')
            ingredienttree.reversearithmetic(promptint())
        # $ this is where results of the arithmetic methods would be printed
        # ? if MODE B and population > 1
        if ingredienttree.population >= 2 and MODE == ProgramState.MODE_B:
            ingredienttree.reformat_output()
            print('\n')
        # ? if MODE A and population > 1
        elif ingredienttree.population >= 2 and MODE == ProgramState.MODE_A:
            print('You can make', ingredienttree.amountresulted, 'of',
                  ingredienttree.ingredient, 'with the materials you have')
            # ? output the endpoint ingredient names and amounts resulted
            for item in ingredienttree.findendpoints({}).items():
                print('You would use',
                      item[1].amountresulted, 'of', item[1].ingredient)
        # ? population == 1
        else:
            print('You would need', ingredienttree.amountresulted, 'to create',
                  ingredienttree.amountresulted, 'of', ingredienttree.ingredient)
        # prompt the user if they want to output the ingredient tree onto A csv file
        print('Do you want to save your tree to create',
              ingredienttree.ingredient, 'to a csv file? (Y/N)')
        while True:
            userinput = input('').strip().upper()
            if userinput not in ('Y', 'N'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      ' character')
            elif userinput == 'Y':
                # change the tree key
                ingredienttree.modifytreekey(
                    ingredienttree.gen_treekey())
                # make sure each ingredient alias is unique
                makealiasunique(ingredienttree)
                # write onto file
                writetreetocsv(ingredienttree)
                break
            else:
                break
        # prompt the user to see if they want to run the program again
        while True:
            userinput = input('\nDo you want to run the program again with'
                              ' another item tree? (Y/N) ').strip().upper()
            if userinput not in ('Y', 'N'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      ' character')
            else:
                break
        if userinput == 'N':
            break
    # close program in 10 seconds
    print('the program will close in 10 seconds')
    NANI: int = 10
    while NANI > 0:
        time.sleep(1)
        NANI -= 1
    print('terminating program')
# end main
