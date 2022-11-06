"""
main script for Python Process Map (v2.0)
"""
import math
import random
import sys
import time
from Enum import enum
class ProgramState(Enum):
    ModeA = 0
    ModeB = 1
#PROGRAMMODETYPE: int = 0


class NodeB:
    """
    replace docstring of this method
    """
    ingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, ingredient: str = '',
                       amountonhand: int = 0,
                       amountparentmadepercraft: int = 1, 
                       amountneeded: int = 1) -> None:
        """
        replace docstring of this method
        """
        self.amountonhand = amountonhand
        self.amountparentmadepercraft = amountparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.amountresulted = 0


class Node(NodeB):
    """
    replace docstring of this method
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    promptamountparentmade: bool = False
    # this is unique identifer for an ingredient tree when its outputted into a csv file
    treekey: str = ''

    def __init__(self, ingredient: str = '',
                       parent=None,
                       amountonhand: int = 0,
                       amountparentmadepercraft: int = 1,
                       amountneeded: int = 1,
                       promptamountparentmade: bool = False) -> None:  # pylint:disable=C0301
        """
        replace docstring of this method
        """
        super().__init__(ingredient,
                        amountonhand,
                        amountparentmadepercraft,
                        amountneeded)
        self.instancekey = Node.instances
        self.children = {}
        self.parent = parent
        if self.parent is not None:
            self.generation = self.parent.generation + 1
            self.parent.children.update({self.instancekey: self})
            self.treekey = self.parent.treekey
        else:
            self.generation = 0
            self.treekey = self.generate_treekey()
        Node.instances += 1
        if __name__ == '__main__':
            self.__inputnumerics(promptamountparentmade)
    def __promptint(self) -> int:
        """
        replace docstring of this method
        """
        while True:
            myinput = input('').strip()
            if not myinput.isdigit():
                print('you can only type in a positive integer')
            else:
                return int(myinput)

    def __inputnumerics(self, promptamountparentmade : bool):
        """
        replace docstring of this method
        """
        # prompt amount on hand
        while True and PROGRAMMODETYPE == 0:
            print('How much', self.ingredient, 'do you have on hand: ')
            self.amountonhand = promptint()
            if self.amountonhand < 0:
                print('That number is not valid')
            else:
                break
        if self.parent is not None:
            # prompt amount made per craft
            while True and promptamountparentmade:
                print('How much', self.parent.ingredient,
                      'do you create each time you craft it: ')
                self.amountparentmadepercraft = promptint()
                if self.amountparentmadepercraft < 1:
                    print('That number is not valid')
                else:
                    break
            # prompt amount needed
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
    @classmethod
    def generate_treekey(cls)->str:
        """
        randomly generates an alpha numeric string to be used as a unique identifier for the tree
        and all nodes linked to this instance
        """
        cls.treekey = ''
        for _ in range(0, 10):
            cls.treekey += random.choice('0123456789abcdefghijklmnopqrstuvwxyz')
        return cls.treekey

def findlocalendpoints(cur: Node, foundendpoints: dict) -> dict:
    """
    replace docstring of this method
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




def recursivearithmetic(cur: Node) -> int:
    """
    replace docstring of this method
    """
    # check and set minimum resulted if queue is not empty
    tentativeinteger: int = sys.maxsize
    if len(cur.queueamountresulted) == 0:
        tentativeinteger = 0
    else:
        for myinteger in cur.queueamountresulted.items():
            if myinteger[1] < tentativeinteger:
                tentativeinteger = myinteger[1]
    red = (cur.amountparentmadepercraft / cur.amountneeded)
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
    replace docstring of this method
    """
    cur.amountresulted = desiredamount
    red: float = ((cur.amountparentmadepercraft/cur.amountneeded)
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

def head(node : Node) -> Node:
    """
    replace docstring of this method
    """
    while node.parent is not None:
        node = node.parent
    return node


def populate(cur: Node) -> Node:
    """
    replace docstring of this method
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
        checkstring = head(tempinstance).ingredient
    # prompt user to input ingredients
    print('What ingredients do you need to create', cur.ingredient, end=':\n')
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
        elif myinput == cur.ingredient:
            print('You cannot type that in')
        elif len(myinput) == 0:
            break
        else:
            inputqueue.update({len(inputqueue): myinput})
    # create new child instances using subpopulate method
    tempbool: bool = True
    for newnodename in inputqueue.items():
        Node(newnodename[1], cur, 0, 1, 1, tempbool)
        tempbool = False
    # continue method runtime
    for child in cur.children.items():
        if not isinstance(child[1], Node):
            raise TypeError('child is not an instance of', Node)
        populate(child[1])
    #return the head node of the tree
    return head(cur)


def subpopulate(node : Node,
                ingredient : str,
                amountmadepercraft : int,
                promptamountmadepercraft : bool) -> Node:
    """
    replace docstring of this method
    """
    # create a dictionary of nodes that have the same ingredient
    # if the dictionary returns {-1:None}, return a default new node
    # else ask the user if the want to create a copy of the node
    # if the user inputs "N", return default node
    # else prompt the user for which node they want to copy and return a clone of that
    return node

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


if __name__ == '__main__':
    print('Welcome to Process Map (Python) v1.1!\n')
    while True:
        # prompt user which mode they want to run the program in
        print('Which mode do you want to use:')
        print('Mode A - You are trying to figure out how much of your desired item you can make with the current supply of materials (Type in A)')  # pylint:disable=C0301
        print('Mode B - You are trying to figure out how much base materials you need to create a certain amount of your desired item, (Type in B)')  # pylint:disable=C0301
        print("Type in 'H' if you need a reminder of the prompt\n")
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
                break
            elif userinput == 'H':
                #print prompt again
                print('Which mode do you want to use:')
                print('Mode A - You are trying to figure out how much of your desired item you can make with the current supply of materials (Type in A)')  # pylint:disable=C0301
                print('Mode B - You are trying to figure out how much base materials you need to create a certain amount of your desired item, (Type in B)')  # pylint:disable=C0301
                print("Type in 'H' if you need a reminder of the prompt\n")
            else:
                PROGRAMMODETYPE = 0
                break
        # prompt user to type in the name of the item they want to create
        while True:
            itemname = input(
                'What is the name of the item you want to create: ')
            itemname = itemname.strip()
            if len(itemname) == 0:
                print('You must type something in')
            else:
                break
        headnode = Node(itemname, None)
        if PROGRAMMODETYPE == 0:  # ? normal program mode
            headnode = populate(headnode)
            for subnode in findlocalendpoints(headnode, {}).items():
                recursivearithmetic(subnode[1])
            print('# resulted of', headnode.ingredient, '',
                  end=str(headnode.amountresulted)+'\n')
        else:  # ? Mode B
            print('How much', headnode.ingredient, 'do you want to create:')
            desirednumber: int = promptint()
            populate(headnode)
            reversearithmetic(headnode, desirednumber)
            # output the results
            print('To get', str(str(desirednumber)+'x'),
                  headnode.ingredient, 'you need the following:')
            results: dict = findlocalendpoints(headnode, {})
            # iterate through the dictionary and output the amounts on hand
            reformat_output(results)
        # prompt the user to see if they want to input another tree
        print("\nDo you want to run the program again with another item tree? (Y/N)")
        print("type in 'H' if you need to be reminded of the prompt")
        while True:
            userinput = input('').strip().upper()
            if userinput not in ('Y', 'N', 'H'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one character')
            elif userinput == 'N' or userinput == 'Y':
                break
        headnode.clearamountresulted()
        if userinput == 'N':
            break
    # terminate the program
    print('terminating process in 10 seconds')
    # close program in 10 seconds
    NANI = 10
    while NANI > 0:
        time.sleep(1)
        NANI -= 1
