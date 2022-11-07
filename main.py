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

    def __init__(self, ingredient: str = '',  # pylint: disable=R0913
                 parent=None,
                 amountonhand: int = 0,
                 amountparentmadepercraft: int = 1,
                 amountneeded: int = 1,
                 promptamountparentmade: bool = False,
                 treekey: str = '') -> None:
        """
        tentative docstring description
        """
        super().__init__(ingredient,
                         amountonhand,
                         amountparentmadepercraft,
                         amountneeded)
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

    def search(self, ingredient: str, results: dict) -> dict:
        """
        tentative docstring description
        """
        # parse through entire tree and find all instances of the ingredient
        for child in self.children.items():
            child[1].search(ingredient, results)
        # if the ingredient is found, add the instance to the results dict
        if self.ingredient == ingredient:
            results.update({self.instancekey: self})
        # if at endpoint node & there's no nodes in results, return {-1:None}
        elif len(self.children) == 0 and len(results) == 0:
            return {-1: None}
        return results
    # end def
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


def secondhead(node: Node) -> Node:
    """
    tentative docstring description
    """
    # check if the node generation is less than 2 or if the population of the
    # the ingredient tree is less than 2 (meaning there's only one ingredient)
    if node.generation < 2 or node.countpopulation() < 2:
        return node
    # traverse upward until the generation is 2
    while node.generation != 2 and node.parent is not None:
        node = node.parent
    return node
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


def locateemplacespot(node: Node, pandaslistrow: list) -> bool:
    """
    tentative docstring description
    """
    # check if the pandaslistrow is the proper length
    if len(pandaslistrow) != len(TESTFILENAME):
        # raise a value error
        raise ValueError(
            'pandaslistrow is not the proper length;'
            ' the list passes contains the following:',
            pandaslistrow)
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
             treekey=pandaslistrow[0])
        return True
    return False
# end def


def csvsearch() -> dict:  # @note search for head nodes in csv file
    """
    tentative docstring description
    """
    # create a dict of head nodes in the ingredient tree
    # if the file is not in the directory, return {-1:None}
    if not os.path.exists(TESTFILENAME):
        return {-1: None}
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
            foundheadpoints.update({green[0]: Node(green[1],
                                                   None,
                                                   green[4],
                                                   green[5],
                                                   green[6], False,
                                                   green[0])})
    # if there are no head nodes found, return {-1:None}
    if len(foundheadpoints) == 0:
        return {-1: None}
    return foundheadpoints
# @ audit-note, for now, dont use this method since it only has 1 reference
# end def


def createtreefromcsv(node: Node) -> Node:  # @note create a tree the csv
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
        locateemplacespot(node, row)
    return head(node)
    # @note the node is from chosen the head node from the csv file prompt
# end def


def populate(node: Node) -> Node:  # pylint: disable=too-many-branches
    """
    tentative docstring description
    """
    inputqueue: dict = {}
    checkstring: str = head(node).ingredient
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
    while True:
        myinput = input('').strip()
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
        elif myinput == node.ingredient:
            print('You cannot type that in')
        elif len(myinput) == 0:
            break
        else:
            inputqueue.update({len(inputqueue): myinput})
    # create new child instances using subpopulate method
    promptamountmadepercraft: bool = True
    amountmadepercraft: int = 0
    for newnodename in inputqueue.items():
        _: Node = subpopulate(node=node,
                              ingredient=newnodename[1],
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
    queryresults: dict = head(node).search(ingredient, {})
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


def superpopulate() -> Node:
    """
    tentative docstring description
    """
    # parse the csv file for head nodes, and create a dict
    foundheadnodes: dict = csvsearch()
    foundheadnodes: dict = {}
    # if the search returns {-1:None} call populate method
    filedoesnotexist: bool = os.path.isfile(TESTFILENAME)
    if foundheadnodes == {-1: None} or not filedoesnotexist:
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
            return populate(Node(itemname, None))
        # return ingredient tree from csv
        # @todo finish this, create method to load ingredient tree from csv
        returntree: Node = createtreefromcsv(userchoices[chosenindex])
        returntree.clearamounts()
        return returntree
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
        # prompt user to type in the name of the item they want to create
        while True:
            itemname = input(
                'What is the name of the item you want to create: ').strip()
            if len(itemname) == 0:
                print('You must type something in')
            else:
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
        print('\nDo you want to run the program again with another item tree?'
              '(Y/N)')
        print("type in 'H' if you need to be reminded of the prompt")
        while True:
            userinput = input('').strip().upper()
            if userinput not in ('Y', 'N', 'H'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      'character')
            elif userinput not in ('Y', 'N'):
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
