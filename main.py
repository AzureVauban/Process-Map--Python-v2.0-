"""
main script for Python Process Map (v2.0)
"""
import csv
import math
import random
import sys
import time

PROGRAMMODETYPE: int = 0


class NodeB:
    """
    class for storing simple data about an item such as its name and how much is needed to create
    its parent
    """
    ingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, name: str = '', red: int = 0, blue: int = 1, yellow: int = 1) -> None:
        """
        Args:
            name (str, optional): name of the item. Defaults to ''.
            red (int, optional): amount of the item you have on hand. Defaults to 0.
            blue (int, optional): amount of the parent item you create each time you craft it.
            Defaults to 1.
            yellow (int, optional): amount of item needed to craft the parent item one time.
            Defaults to 1.
        """
        self.amountonhand = red
        self.amountmadepercraft = blue
        self.amountneeded = yellow
        self.queueamountresulted = {}
        self.ingredient = name
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

    def __init__(self, name: str = '', par=None, red: int = 0, blue: int = 1, yellow: int = 1, green: bool = False) -> None:  # pylint:disable=C0301
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
            green (bool,optional): boolean variable, checks if one of the Node's sibiling
            instances was prompted to input the amount made per craft (blue)
        """
        super().__init__(name, red, blue, yellow)
        self.instancekey = Node.instances
        self.children = {}
        self.parent = par
        if self.parent is not None:
            self.generation = self.parent.generation + 1
            self.parent.children.update({self.instancekey: self})
            self.treekey = self.parent.treekey
        else:
            self.generation = 0
            self.treekey = self.generate_treekey()
        self.askmadepercraftquestion = green
        Node.instances += 1
        if __name__ == '__main__':
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
                self.amountmadepercraft = promptint()
                if self.amountmadepercraft < 1:
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

    @classmethod
    def generate_treekey(cls) -> str:
        """
        randomly generates an alpha numeric string to be used as a unique identifier for the tree
        and all nodes linked to this instance
        """
        cls.treekey = ''
        for _ in range(0, 10):
            cls.treekey += random.choice(
                '0123456789abcdefghijklmnopqrstuvwxyz')
        return cls.treekey + '\n'
    # make a method to return a list with all the info needed on a line of the csv file
    def create_info_csv
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
    red = (cur.amountmadepercraft / cur.amountneeded)
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
    """find how much of a material you will need get a particular amount of an item you want

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
    red: float = ((cur.amountmadepercraft/cur.amountneeded)
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
        Node(newnodename[1], cur, 0, 1, 1, tempbool)
        tempbool = False
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


def tentativemethod(node: Node):
    """method that writes to the .csv file

    Args:
        node (Node): stores information about the an ingredient
    """
    print(node.ingredient)


if __name__ == '__main__':
    print('Welcome to Process Map (Python) v1.1!\n')
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
                break
            elif userinput == 'H':
                printprompt()
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
        head = Node(itemname, None)
        if PROGRAMMODETYPE == 0:  # ? normal program mode
            populate(head)
            for subnode in findlocalendpoints(head, {}).items():
                recursivearithmetic(subnode[1])
            print('# resulted of', head.ingredient, '',
                  end=str(head.amountresulted)+'\n')
        else:  # ? Mode B
            print('How much', head.ingredient, 'do you want to create:')
            desirednumber: int = promptint()
            populate(head)
            reversearithmetic(head, desirednumber)
            # output the results
            print('To get', str(str(desirednumber)+'x'),
                  head.ingredient, 'you need the following:')
            results: dict = findlocalendpoints(head, {})
            # iterate through the dictionary and output the amounts on hand
            reformat_output(results)
        # prompt the user to see if they want to input another tree
        print("\nDo you want to run the program again with another item tree? (Y/N)")
        print("type in 'H' if you need to be reminded of the prompt")
        while True:
            userinput = (input(''))
            userinput = userinput.strip()
            userinput = userinput.upper()
            if userinput not in ('Y', 'N', 'H'):
                print("That input is not valid, please type in 'Y' or 'N'")
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
    NANI = 10
    while NANI > 0:
        time.sleep(1)
        NANI -= 1
