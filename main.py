"""
main script for Python Process Map (v2.0)
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
    MODE_A = 0
    MODE_B = 1


PROGRAMSTATE: Enum = ProgramState.MODE_A
TESTFILENAME: str = 'ingredient_trees_processmap.csv'
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


class Node(NodeB):  # pylint: disable=R0902
    """
    tentative docstring description
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    promptamountparentmade: bool = False
    # this is unique identifer for an ingredient tree when its outputted to a
    # csv file
    treekey: str = ''
    isfromcsvfile: bool = False

    def __init__(self, ingredient: str = '',  # pylint: disable=R0913
                 parent=None,
                 amountonhand: int = 0,
                 amountparentmadepercraft: int = 1,
                 amountneeded: int = 1,
                 promptamountparentmade: bool = False,
                 treekey: str = '',
                 isfromcsvfile: bool = False) -> None:
        """
        tentative docstring description
        """
        super().__init__(ingredient,
                         amountonhand,
                         amountparentmadepercraft,
                         amountneeded)
        self.isfromcsvfile = isfromcsvfile
        self.treekey = treekey
        self.instancekey = Node.instances
        self.children = {}
        self.parent = parent
        if self.parent is not None:
            self.generation = self.parent.generation + 1
            self.parent.children.update({self.instancekey: self})
            self.treekey = self.parent.treekey
        else:
            self.generation = 0
            if self.treekey == '':
                self.treekey = self.generate_treekey()
        Node.instances += 1
        if __name__ == '__main__':
            self.__inputnumerics(promptamountparentmade)
    # end def

    def __inputnumerics(self, promptamountparentmade: bool):
        """
        tentative docstring description
        """
        # prompt amount on hand
        while PROGRAMSTATE == 0:
            print('How much', self.ingredient, 'do you have on hand: ')
            self.amountonhand = promptint()
            if self.amountonhand < 0:
                print('That number is not valid')
            else:
                break
        if self.parent is not None and promptamountparentmade:
            # prompt amount made per craft
            while True:
                print('How much', self.parent.ingredient,
                      'do you create each time you craft it: ')
                self.amountparentmadepercraft = promptint()
                if self.amountparentmadepercraft < 1:
                    print('That number is not valid')
                else:
                    break
        if self.parent is not None:
            # prompt amount needed
            while True:
                print('How much', self.ingredient, 'do you need to craft',
                      self.parent.ingredient, '1 time: ')
                self.amountneeded = promptint()
                if self.amountneeded < 1:
                    print('That number is not valid')
                else:
                    break
    # end def

    def clearamounts(self):
        """
        tentative docstring description
        """
        self.queueamountresulted.clear()
        self.amountonhand = 0
        self.amountresulted = 0
        if len(self.children) > 0:
            for child in self.children.items():
                if not isinstance(child[1], Node):
                    raise TypeError('Child is not an instance of', Node)
                child[1].clearamounts()
    # end def

    @classmethod
    def generate_treekey(cls) -> str:
        """
        tentative docstring description
        """
        cls.treekey = ''
        for _ in range(0, 10):
            cls.treekey += random.choice(
                '0123456789abcdefghijklmnopqrstuvwxyz')
        return cls.treekey
    # end def

    def findlocalendpoints(self, foundendpoints: dict) -> dict:
        """
        tentative docstring description
        """
        if len(self.children) > 0:
            for child in self.children.items():
                if not isinstance(child[1], Node):
                    raise TypeError('child is not an instance of', Node)
                child[1].findlocalendpoints(foundendpoints)
        else:
            foundendpoints.update({self.instancekey: self})
        return foundendpoints
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

    def countpopulation(self, population: int = 0) -> int:
        """
        tentative docstring description
        """
        population += 1
        for child in self.children.items():
            child[1].countpopulation(population)
        return population
    # end def

    def modifytreekey(self, newtreekey: str):
        """
        tentative docstring description
        """
        # modify the tree keys in each node in the tree so when its written to
        # the csv file if will have a differing key from its original tree
        self.treekey = newtreekey
        for child in self.children.items():
            child[1].modifytreekey(newtreekey)
    # end def

    def reformat_output(self):
        """
        tentative docstring description
        """
        # set the new dictionary to be empty
        red_dict: dict = {}
        # set the new dictionary to have unique ingredients as keys
        # and a list of tuples of the parent of said endpoint instance and the
        # amount on hand as values
        for node in self.findlocalendpoints({}).items():
            if node[1].ingredient not in red_dict:
                red_dict.update(
                    {node[1].ingredient: [(node[1].parent.ingredient,
                                           node[1].amountonhand)]})
            else:
                red_dict[node[1].ingredient].append(
                    (node[1].parent.ingredient,
                     node[1].amountonhand))

        output_dictionary: dict = {}
        for item in red_dict.items():
            orangeinteger: int = 0  # sum of the amount on hand all tuple items
            for orangenumber in item[1]:
                orangeinteger += orangenumber[1]
            for orangetuple in item[1]:
                if item[0] not in output_dictionary:
                    output_dictionary.update({item[0]: [str(round(
                        (orangetuple[1]/orangeinteger)*100, 2)) +
                        '% ('+str(orangetuple[1])+'x) used in ' +
                        orangetuple[0]]})
                else:  # if item is in the dict, append the string to list
                    output_dictionary[item[0]].append(
                        str(round((orangetuple[1]/orangeinteger)*100, 2)) +
                        '% ('+str(orangetuple[1])+'x) used in ' +
                        orangetuple[0])
        # output the dictionary keys and values
        for item in output_dictionary.items():
            print(item[0], end=' (')
            for index, string in enumerate(item[1]):
                if index == len(item[1])-1:
                    print(string, end='')
                else:
                    print(string, end=', ')
            print(')')
    # end def

    def csv_createrowdict(self) -> dict:
        """
        tentative docstring description
        """
        pandasrowdict: dict = {}
        pandasrowdict.update({'Tree_Key': self.treekey})
        pandasrowdict.update({'Ingredient': self.ingredient})
        pandasrowdict.update({'Ingredient_Alias': self.aliasingredient})
        if self.parent is not None:
            pandasrowdict.update(
                {'Parent_of_Ingredient': self.parent.ingredient})
        else:
            pandasrowdict.update({'Parent_of_Ingredient': 'None'})
        pandasrowdict.update({'Amount_on_Hand': str(self.amountonhand)})
        pandasrowdict.update(
            {'Amount_Made_Per_Craft': str(self.amountparentmadepercraft)})
        pandasrowdict.update(
            {'Amount_Needed_Per_Craft': str(self.amountneeded)})
        pandasrowdict.update({'Generation': str(self.generation)})
        return pandasrowdict
    # end def

    def csv_createrowsdicts(self, pandasrows: list) -> list:
        """
        tentative docstring description
        """
        pandasrows.append(self.csv_createrowdict())
        for child in self.children.items():
            child[1].csv_createrowsdicts(pandasrows)
        # if odd amount of nodes, reverse the list
        if not len(pandasrows) // 2 == 0:
            return pandasrows[::-1]
        return pandasrows
    # end def

    def output_tree_to_csv(self):
        """
        tentative docstring description
        """
        # if the file is not in the directory, create it
        if not os.path.exists(TESTFILENAME):
            # create the file
            pandas.DataFrame(columns=FIELDNAMES).to_csv(
                TESTFILENAME, index=False)
        # then write to the file but calling the method again recursively
        for row in self.csv_createrowsdicts([]):
            pandas.DataFrame(row, index=[0]).to_csv(
                TESTFILENAME, mode='a', header=False, index=False)
    # end def

    def returnlistofalias(self, ingredient: str, tempname: list) -> list:  # noqa: E501
        """
        tentative docstring description
        """
        if self.aliasingredient == ingredient:
            tempname.append((self.instancekey, self))
        for child in self.children.items():
            child[1].returnlistofalias(ingredient, tempname)
        return tempname
    # end def
# end def


def search(node: Node, ingredient: str, results: dict) -> dict:
    """
    tentative docstring description
    """
    # parse through entire tree and find all instances of the ingredient
    if node.ingredient == ingredient:
        # if the ingredient is found
        # add the instance to the results dict
        results.update({node.instancekey: node})
    # keep searching through the ingredient tree
    for subnode in node.children.items():
        search(subnode[1], ingredient, results)
    return results
# end def


def promptint() -> int:
    """
    tentative docstring description
    """
    while True:
        myinput = input('').strip()
        if not myinput.isdigit():
            print('you can only type in a positive integer')
        elif int(myinput) < 0:
            print('[please type in a postive integer')
        else:
            return int(myinput)
# end def


def head(node: Node) -> Node:
    """
    tentative docstring description
    """
    while node.parent is not None:
        node = node.parent
    return node
# end def


def makeallaliasunique(node: Node):
    """
    tentative docstring description
    """
    # recursively call for all children
    aliaslist: list = head(node).returnlistofalias(node.ingredient, [])
    # if the size of the list returned is greater than 1
    if len(aliaslist) > 1:
        # organize nodes based on instancekey (least to greatest)
        for red in aliaslist:
            for blue in aliaslist:
                if red[1].instancekey > blue[1].instancekey:
                    # swap the indicies
                    blue, red = red, blue
        # then change the alias of the nodes to be unique
        for index, name in enumerate(aliaslist):
            # if the index is 0, then it's the original node
            if index != 0:
                name.aliasingredient = name.ingredient + \
                    ' (' + str(index+1) + ')'

    for child in node.children.items():
        makeallaliasunique(child[1])
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
                           amountparentmadepercraft=False)
    # create a copy of all the children of the parameter node
    for subnode in node.children.items():
        childsubnode: Node = Node(ingredient=subnode[1].ingredient,
                                  parent=subnode,
                                  amountonhand=subnode[1].amountonhand,
                                  amountneeded=subnode[1].amountneeded,
                                  amountparentmadepercraft=subnode[1].amountparentmadepercraft,  # noqa: E501 #pylint: disable=line-too-long
                                  promptamountparentmade=False)
        print('creating', childsubnode.ingredient, 'data...')
    return clonenode
# end def


def locate_emplace_spot(node: Node, pandaslistrow: list) -> bool:
    """
    tentative docstring description
    """
    # check if the pandaslistrow is the proper length
    if len(pandaslistrow) != 8:
        # raise a value error
        raise ValueError(
            'pandaslistrow is not the proper length;'
            ' the list passed contains the following:',
            pandaslistrow,
            'which has a length of', len(pandaslistrow),
            'and not the proper length of', len(FIELDNAMES))
    # remove any underscores from the ingredient
    pandaslistrow[1] = pandaslistrow[1].replace('_', ' ')
    # remove any underscores from the parent of the ingredient
    pandaslistrow[3] = pandaslistrow[3].replace('_', ' ')
    # check if the current node is the parent of the ingredient
    foundemplacelocation: bool = node.treekey == pandaslistrow[
        0] and pandaslistrow[3] != 'None' and pandaslistrow[
        3] == node.ingredient and pandaslistrow[7] > 0 and node is not None
    if foundemplacelocation:
        # @note somewhere in the project it needs to be determined if the user
        # will allow the amount on hands from the csv file to be used or if
        # the user will input the amount on hand themselves
        Node(pandaslistrow[1],
             parent=node,
             amountneeded=pandaslistrow[6],
             amountparentmadepercraft=pandaslistrow[5],
             amountonhand=pandaslistrow[4],
             treekey=pandaslistrow[0],
             isfromcsvfile=True)
        return True
    return False
# end def


def csvsearch() -> dict:
    """
    tentative docstring description
    """
    # create a dict of head nodes in the ingredient tree
    # if the file is not in the directory, return {-1:None}

    # if there are nodes found, return the dict, else return {-1:None}
    foundheadpoints: dict = {}
    # iterate through the rows of the dataframe
    for purple in pandas.read_csv(TESTFILENAME).to_dict('index').items():
        # convert the values of the dictionary to a list
        green: list = list(purple[1].values())
        # if the conditions are met for it to mock a head node
        if green[3] == 'None' and green[5] == 1 and green[
                6] == 1 and green[7] == 0:
            # create a node from the row's data
            # add the node to the dictionary of head nodes
            foundheadpoints.update({green[0]: Node(ingredient=green[1],
                                                   parent=None,
                                                   promptamountparentmade=False,  # noqa: E501 #pylint: disable=line-too-long
                                                   treekey=green[0],
                                                   isfromcsvfile=True)})
    # if there are no head nodes found, return {-1:None}
    if len(foundheadpoints) != 0:
        return foundheadpoints
    return {-1: None}
# @ audit-note, for now, dont use this method since it only has 1 reference
# end def


def createtreefromcsv(node: Node) -> Node:
    """
    tentative docstring description
    """
    # open the file and read the rows to create a list of rows with matching
    # treekeys as the selected node
    sublist: list = []
    # ? list of rows that match the head node's tree key
    # iterate through the rows of the dataframe
    for purple in pandas.read_csv(TESTFILENAME).to_dict('index').items():
        # convert the values of the dictionary to a list
        green: list = list(purple[1].values())
        # if the tree key of the row matches the head node's tree key
        if green[0] == node.treekey:
            sublist.append(green)
        # for each row, check if the it meets the conditions to be a child
        # node of the head node
    for row in sublist:
        locate_emplace_spot(node, row)
    return head(node)
# end def


def populate(node: Node, modifyingpreset: bool = False) -> Node:
    """
    tentative docstring description
    """
    # output ingredient trail
    if node.parent is not None:
        tempnode: Node = node
        print('TRAIL: ', end='')
        while True:
            if tempnode.parent is not None:
                print(tempnode.ingredient, '-> ', end='')
                tempnode = tempnode.parent
            else:
                print(tempnode.ingredient)
                break
    # prompt user to input ingredients
    print('What ingredients do you need to create', node.ingredient, end=':\n')
    # if modifying a preset, print out subnode ingredients already in
    if modifyingpreset and len(node.children) > 0:
        print('NOTE: The following ingredients are already in the preset:')
        for subnode in node.children.items():
            print(subnode[1].ingredient)
        print('\n')

    # @note duplicate inputs arent failing the validation check
    userinputlist: list = []
    while True:
        # if the input is empty, break the loop
        myinput: str = input('').strip()
        # if the length of the user inputs is greator than or equal to 2
        # check to see if the ussr input is valid,
        if myinput in [head(node).ingredient, node.ingredient]:  # noqa: E501 #pylint: disable=line-too-long
            print('Invalid input, we are trying to make that item!')
        # if the length of the user input is 0, break the loop
        elif myinput in userinputlist:
            print('Invalid input, duplicate inputs!')
        elif len(myinput) == 0:
            break
        else:
            # if the condition is met, append the input to the list
            userinputlist.append(myinput)
    # create new child instances using subpopulate method
    promptamountmadepercraft: bool = True
    amountmadepercraft: int = 0
    for newnodename in userinputlist:
        _: Node = subpopulate(node=node,
                              ingredient=newnodename,
                              amountmadepercraft=amountmadepercraft,
                              promptamountmadepercraft=promptamountmadepercraft)  # noqa: E501 #pylint: disable=line-too-long
        if promptamountmadepercraft:
            promptamountmadepercraft = False
            amountmadepercraft = _.amountparentmadepercraft
    # continue method runtime
    for child in node.children.items():
        if not isinstance(child[1], Node):
            raise TypeError('child is not an instance of', Node)
        populate(child[1])
    # make each alias in the ingredient tree unique
    makeallaliasunique(node)
    # return recursive math method of function if in program mode A
    if PROGRAMSTATE == ProgramState.MODE_A:
        # you this this because once it reaches the code, this node will be an
        # endpoint, reducing the need to parse through the tree for endpoint
        # nodes outside of the populate method
        node.recursivearithmetic()
    # return the head node of the tree
    return head(node)
# end def


def subpopulate(node: Node,
                ingredient: str,
                amountmadepercraft: int,
                promptamountmadepercraft: bool) -> Node:
    """
    tentative docstring description
    """
    # search for nodes in the ingredient tree with the same ingredient name

    queryresults: dict = search(ingredient=ingredient,
                                node=node,
                                results={})
    if len(queryresults) == 0:
        queryresults = {-1: None}
    if queryresults == {-1: None} or node.parent is None:
        # if no nodes are found, return a default node
        # if the node is the head node, return a default node
        return Node(ingredient, node,
                    0, 1,  # amount on hand, amount needed
                    amountmadepercraft,
                    promptamountmadepercraft)
    # if there are nodes found, dict -> list & prompt user choose a node
    userchoices: list = []
    for subnode in queryresults.items():
        userchoices.append(subnode[1])
    print('Which of the following do you want to use (valid choice must be a'
          ' number between 1 and', len(userchoices), end='):\n')
    # print out the list of nodes
    pos: int = 1
    for subnode in userchoices:
        if subnode.parent is None or not isinstance(subnode.parent, Node):
            raise ValueError(
                'parent of subnode must be a body or endpoint instance of',
                Node)
        print(pos, '.', subnode.parent.ingredient)
    pos += 1
    print()
    # check input
    while True:
        # if the input is within range, return the node at the index
        chosenindex: int = promptint() - 1
        # if the input is less than 0 or greater than the length of the list
        if chosenindex < 0 or chosenindex > len(userchoices):
            # if input is out of range for the list, return a default node
            return Node(ingredient,
                        node, 0, 1,  # amount on hand, amount needed
                        amountmadepercraft,
                        promptamountmadepercraft)
        # return a clone of the node at a chosen index
        return clone(userchoices[chosenindex])
    # code here should be unreachable
# end def


def superpopulate() -> Node:  # pylint: disable=too-many-branches
    """
    tentative docstring description
    """
    # parse the csv file for head nodes, and create a dict
    foundheadnodes: dict = {}
    # iterate through the rows of the dataframe
    if os.path.isfile(TESTFILENAME):
        for purple in pandas.read_csv(TESTFILENAME).to_dict('index').items():
            # convert the values of the dictionary to a list
            green: list = list(purple[1].values())
            # if the conditions are met for it to mock a head node
            if green[3] == 'None' and green[5] == 1 and green[
                    6] == 1 and green[7] == 0:
                # create a node from the row's data
                # add the node to the dictionary of head nodes
                foundheadnodes.update({green[0]: Node(ingredient=green[1],
                                                      parent=None,
                                                      promptamountparentmade=False,  # noqa: E501
                                                      treekey=green[0])})
    # if there are no head nodes found, set to {-1:None}
    if len(foundheadnodes) == 0:
        foundheadnodes.update({-1: None})
    # if the search returns {-1:None} call populate method
    newtreeprompt: str = 'What is the name of the item you want to create: '
    if foundheadnodes == {-1: None} or not os.path.isfile(TESTFILENAME):
        # prompt user to type in the name of the item they want to create
        while True:
            itemname = input(newtreeprompt).strip()
            if len(itemname) == 0:
                print('You must type something in')
            else:
                break
        return populate(Node(itemname, None))
    # else convert dict to list and prompt the user to choose an ingredient
    userchoices: list = []
    for node in foundheadnodes.items():
        userchoices.append(node[1])
    print('Which of the following do you want to use (valid choice must be a'
          ' number between 1 and', len(userchoices), end='):\n')
    # print out the list of nodes
    pos: int = 1
    for subnode in userchoices:
        if subnode.parent is not None:
            raise ValueError(
                'node from csv must be a head instance of', Node)
        print(pos, '.', subnode.ingredient)
        pos += 1
    # prompt the user for a choice of head node
    while True:
        chosenindex: int = promptint() - 1
        # if the user did not choose a valid index, create ingredient tree
        # manually
        if chosenindex < 0 or chosenindex > len(userchoices):
            # prompt user to type in the name of the item they want to create
            while True:
                itemname = input(newtreeprompt).strip()
                if len(itemname) == 0:
                    print('You must type something in')
                else:
                    break
            return populate(Node(itemname, None))
        # return ingredient tree from csv
        returntree: Node = createtreefromcsv(userchoices[chosenindex])
        # change the tree key of each node
        returntree.modifytreekey(returntree.generate_treekey())
        # clear amount on hand and amount resulted
        returntree.clearamounts()
        # add bool to check if modify a created tree from the csv file
        return populate(returntree)
    # code here should be unreachable
# end def


if __name__ == '__main__':
    print('Welcome to Process Map (Python) v1.1!\n')
    # main loop
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
                PROGRAMSTATE = ProgramState.MODE_B
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
                PROGRAMSTATE = ProgramState.MODE_A
                break
        # populate tree
        headnode: Node = superpopulate()
        if PROGRAMSTATE == ProgramState.MODE_A:  # ? normal program mode
            print('# resulted of', headnode.ingredient, '',
                  end=str(headnode.amountresulted)+'\n')
        else:  # ? Mode B
            print('How much', headnode.ingredient, 'do you want to create:')
            desirednumber: int = promptint()
            # populate(headnode)
            headnode.reversearithmetic(desirednumber)
            # output the results
            print('To get', str(str(desirednumber)+'x'),
                  headnode.ingredient, 'you need the following:')
            # iterate through the dictionary and output the amounts on hand
            headnode.reformat_output()
        # prompt if the user wants to output their tree into a csv file
        print('Do you want to save your tree to create',
              headnode.ingredient, 'to a csv file? (Y/N)')
        while True:
            userinput = input('').strip().upper()
            if userinput not in ('Y', 'N'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      'character')
            elif userinput == 'Y':
                # write onto file
                headnode.output_tree_to_csv()
                break
            else:
                break
        headnode.clearamounts()
        # prompt the user to see if they want to input another tree
        while True:
            userinput = input('\nDo you want to run the program again with'
                              ' another item tree? (Y/N) ').strip().upper()
            if userinput not in ('Y', 'N'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      'character')
            else:
                break
        if userinput == 'N':
            break
    # terminate the program
    print('terminating process in 10 seconds')
    # close program in 10 seconds
    NANI = 10
    while NANI > 0:
        time.sleep(1)
        NANI -= 1
