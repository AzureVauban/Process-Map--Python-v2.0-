"""Reformat of main.py
- functional programming
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
    tentative docstring description
    """
    MODE_A = 0  # recursive arithmetic (amountresulted)
    MODE_B = 1  # inverse recursive arithmetic (amountonhand)


MODE: ProgramState = ProgramState.MODE_A
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
# end def


class NodeB:  # pylint: disable=R0903
    """
    tentative docstring description
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
        tentative docstring description
        """
        self.amountonhand = amountonhand
        self.amountparentmadepercraft = amountparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.amountresulted = 0
        self.aliasingredient = ingredient.replace(' ', '_')
    # end def
# end def


class Node(NodeB):  # pylint: disable=R0913
    """
    tentative docstring description
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    treekey: str = ''
    isfromcsvfile: bool = False
    treepopulation: int = 1

    def __init__(self, ingredient: str = '',  # pylint: disable=R0913
                 parent=None,
                 amountonhand: int = 0,
                 amountparentmadepercraft: int = 1,
                 amountneeded: int = 1,
                 promptamountparentmade: bool = False,  # pylint:disable=W0613
                 promptamountsOn: bool = False,
                 isfromcsvfile: bool = False,
                 treekey: str = '') -> None:
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
                self.treekey = self.generate_treekey()
        if promptamountsOn and __name__ == '__main__':
            # only prompt the user to set the amounts if running in main
            # module and the boolean is true
            pass
        Node.instances += 1
    # end def

    @classmethod
    def generate_treekey(cls, maxlength: int = random.randint(10, 20)) -> str:
        """
        generate a unique tree key of random alphumeric characters
        """
        cls.treekey = ''
        for _ in range(0, maxlength):
            cls.treekey += random.choice(
                '0123456789abcdefghijklmnopqrstuvwxyz')
        return cls.treekey
    # end def

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
    # end def

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
    # end def

    def changetreekey(self, newtreekey: str):
        """
        change the tree key of the node and all of its children
        """
        self.treekey = newtreekey
        for subnode in self.children.items():
            subnode[1].changetreekey(newtreekey)

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
    # end def

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
# end def


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
    # end def


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
# end def


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
# end def


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
# end def


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
# end def


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
        node (Node): _description_
        pandasrow (list): _description_

    Raises:
        TypeError: _description_

    Returns:
        bool: _description_
    """
    if len(pandasrow) != len(FIELDNAMES):
        raise TypeError('The row of data is not the correct length')
    # remove any underscores from the ingredient
    pandasrow[1] = pandasrow[1].replace('_', ' ')
    # remove any underscores from the parent of the ingredient
    pandasrow[3] = pandasrow[3].replace('_', ' ')
    foundemplacelocation: bool = node.treekey == pandasrow[0] and pandasrow[
        3] != 'None' and pandasrow[3] == node.ingredient and pandasrow[7] > 0 and node is not None
    if foundemplacelocation:
        # @note somewhere in the project it needs to be determined if the user
        # will allow the amount on hands from the csv file to be used or if
        # the user will input the amount on hand themselves
        Node(pandasrow[1],
             parent=node,
             amountneeded=pandasrow[6],
             amountparentmadepercraft=pandasrow[5],
             amountonhand=pandasrow[4],
             treekey=pandasrow[0],
             # isfromcsvfile=True,
             promptamountsOn=False)
        return True
    else:
        for subnode in node.children.items():
            createtree(subnode[1], pandasrow)
    return False


def treepop(node: Node, population: int = 0) -> int:
    """
    returns the amount of nodes within an ingredient tree

    Args:
        node (Node): stores information about an ingredient
        population (int, optional): amount of nodes counted. Defaults to 0.

    Returns:
        int: the current population of the ingredient tree
    """
    population += 1
    for subnode in node.children.items():
        treepop(subnode[1], population)
    return population
# end def


def createtreefromcsv(parent: Node) -> Node:  # todo debug this method
    """
    figures out where to create and link a new node from the csv file

    Args:
        parent (Node): potential parent node to link new node to
        pandasrow (list): data from csv file, creates node from it

    Returns:
        Node: parent most node of the tree
    """
    # todo - debug this method (creates tree incorrectly (LACKS GEN>2 NODES))
    # check if the row has the correct amount of elements
    # the node must match the following requirements to link:
    # parent ingredient must be the same as the parent ingredient
    # treekey must be the same
    # generation must be greater than 0
    sublist: list = []
    for purple in pandas.read_csv(FILENAME).to_dict('index').items():
        # convert the values of the dictionary to a list
        green: list = list(purple[1].values())
        # if the tree key of the row matches the head node's tree key
        if green[0] == parent.treekey and green[3] != 'None':
            # the sublist contains node only from the tree
            sublist.append(green)
    # figure out where to emplace the node
    # * correctly finds all nodes with the same treekey from the csv file
    for index, row in enumerate(sublist):
        createtree(parent, row)
        # sublist.remove(sublist[index])
        red: str = str('\x1B[31m'+row[3]+'\x1B[0m')  # parent ingredient name
        blue: str = str('\x1B[36m'+row[1]+'\x1B[0m')  # ingredient name
        print('emplaced node', index, red+' | ' + blue)
        # sublist.remove(sublist[index])
        print('Current population of tree: \x1B[33m', end=str(
            treepop(parent))+'\x1B[0m\n')
    print('Current population of tree: \x1B[33m', end=str(
            treepop(parent))+'\x1B[0m\n')
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
    if node.parent is not None and node.ingredient == ingredient[0]:
        for subnode in node.children.items():
            results.append(subnode[1])
    # recrusively keep searching for nodes
    for subnode in node.children.items():
        search(subnode[1], ingredient, results)
    return results
# end def


def clone(node: Node) -> Node:
    """
    tentative docstring description
    """
    # create a copy of the parameter node
    clonenode: Node = Node(ingredient=node.ingredient,
                           parent=node.parent,
                           amountonhand=node.amountonhand,
                           amountneeded=node.amountneeded,
                           amountparentmadepercraft=False,
                           isfromcsvfile=node.isfromcsvfile,
                           promptamountsOn=False)
    # create a copy of all the children of the parameter node
    for subnode in node.children.items():
        childsubnode: Node = Node(ingredient=subnode[1].ingredient,
                                  parent=subnode,
                                  amountonhand=subnode[1].amountonhand,
                                  amountneeded=subnode[1].amountneeded,
                                  amountparentmadepercraft=subnode[1].amountparentmadepercraft,  # noqa: E501 #pylint: disable=line-too-long
                                  promptamountparentmade=False,
                                  isfromcsvfile=subnode[1].isfromcsvfile,
                                  promptamountsOn=False)
        print('creating', childsubnode.ingredient, 'data...')
    return clonenode
# end def


def subpopulate(node: Node, ingredient: str, parseresults: list) -> Node:
    """
    create a subnode and link it to the parent node

    Args:
        node (Node): parent Node to link back to

    Returns:
        Node: new subnode to link back to the parent Node
    """
    # create a list of subnodes that have the same ingredient as the parameter
    # if the list is empty return a defaultly created new node Node
    # !parseresults: list = search(node, ingredient, [])
    for subnode in parseresults:
        if not isinstance(subnode, Node):
            raise TypeError('item in the list is not an instance of', Node)
    if len(parseresults) == 0:
        return Node(ingredient, node)
    # else, prompt the user to create a linkable clone of the new node
    for index, subnode in enumerate(parseresults):
        # output the choices of subnodes:
        # parent ingredient, amountneeded, amountmadepereachcraft
        print(index+1, str('. ' + subnode.parent.ingredient
                           + '|' + str(subnode.amountneeded)
                           + '|' + str(subnode.amountparentmadepercraft)))
    userchoice: int = int(input('Choose a subnode to clone: '))
    userchoice -= 1
    # if the user chooses to create a new node, return a clone subnode
    if userchoice < 0 or userchoice > len(parseresults)-1:
        # if the user did not input a valid index
        # if not return the defaultly created new node
        return Node(ingredient, node)
    return clone(parseresults[userchoice])
# end def


def populate(node: Node) -> Node:  # pylint: disable=R0912
    """create a tree of Nodes

    Args:
        node (Node): parent the subnodes will be linked to

    Returns:
        Node: the head of the ingredient tree
    """
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
        # if ingredient[1] is False, the ingredient is not already in the tree
        if not ingredient[1]:
            searchresults: list = search(head(node), ingredient[0], [])
            # todo debug interaction with the search method
            _ = subpopulate(node, ingredient[0], searchresults)
            # @audit remove this later (for debugging)
            print('created a new node at', _)
    # recrusively continue to populate the tree
    for subnode in node.children.items():
        populate(subnode[1])
    # if the program Mode is A and the length of the children Nodes are 0
    # @note call recursive arithmetic method here
    if MODE == ProgramState.MODE_A and len(node.children) == 0:
        # call the arithmetic method
        node.recursivearithmetic()
    # return the head of the ingredient tree
    return head(node)
# end def


def superpopulate() -> Node:  # todo finish this
    """
    creates an ingredient tree and returns its head node

    Returns:
        Node: head node of the populated ingredient tree
    """
    # check to see if there is a csv file in the current directory
    if not os.path.exists(FILENAME):
        # if the file exists, parse it for head nodes
        nodetree: Node = head(populate(Node(promptheadname())))
        nodetree.changetreekey(nodetree.generate_treekey())
        return nodetree
    # parse the csv file for head nodes
    foundheadnodes: dict = parsecsv()
    # if there are no head nodes {-1:None}
    if foundheadnodes == {-1: None}:
        # return new ingredient tree
        nodetree: Node = head(populate(Node(promptheadname())))
        nodetree.changetreekey(nodetree.generate_treekey())
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
            if treepop(head(userchoices[blue]), 0) < treepop(head(userchoices[red]), 0):
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
        nodetree.changetreekey(nodetree.generate_treekey())
        return nodetree
    # return the head node of the chosen tree
    # create ingredient tree out of the csv file
    nodetree: Node = head(populate(createtreefromcsv(userchoices[userchoice])))
    nodetree.changetreekey(nodetree.generate_treekey())
    return nodetree


if __name__ == '__main__':
    # prompt program mode
    print('Welcome to Process Map (Python) v1.1!\n')
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
        useringredienttree: Node = superpopulate()
        # if the programde mode is B
        if MODE == ProgramState.MODE_B:
            # prompt the user for how much an item they want to make
            print('How much of the item do you want to make?')
            useringredienttree.reversearithmetic(promptint())
        # prompt the user if they want to output the ingredient tree onto A csv file
        print('Do you want to save your tree to create',
              useringredienttree.ingredient, 'to a csv file? (Y/N)')
        while True:
            userinput = input('').strip().upper()
            if userinput not in ('Y', 'N'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      ' character')
            elif userinput == 'Y':
                # change the tree key
                useringredienttree.changetreekey(
                    useringredienttree.generate_treekey())
                # write onto file
                writetreetocsv(useringredienttree)
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
