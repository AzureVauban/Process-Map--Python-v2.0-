"""
Rework for Python 3.11.0
- Merge into development branches once completed
- save working stabe backup of solution.py before merging into development branches into the Stable branch
"""
import random
import sys
import math
FIELDNAMES: list = [  # list of field names for the csv output file
    'Tree_Key',  # 74nry8keki',
    'Ingredient',  # Copper Wire
    'Ingredient_Alias',  # Copper_Wire__ZpgMzAwQdfRu
    'Parent_of_Ingredient',  # Silicon Board
    'Amount_on_Hand',  # 0
    'Amount_Made_Per_Craft',  # 9
    'Amount_Needed_Per_Craft',  # 0
    'Generation'  # 1
]
CSVFILENAME: str = 'output.csv'  # output of  csv file name
GLOBALNODEDICT: dict = {}  # use for searching for nodes in populate method


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


class basicNode():
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
    amountmadepercraft: int = 0
    amountresulted: int = 0
    # key, ingredient, value integer amount of resulted number from previous Node
    queueamountresulted: dict = {}

    def __init__(self, ingredient: str = '', amountonhand: int = 0, amountmadepercraft: int = 0, amountneeded: int = 0) -> None:
        """_summary_

        Args:
            ingredient (str, optional): _description_. Defaults to ''.
            amountonhand (int, optional): _description_. Defaults to 0.
            amountmadepercraft (int, optional): _description_. Defaults to 0.
            amountneeded (int, optional): _description_. Defaults to 0.
        """
        self.ingredient = ingredient
        self.amountonhand = amountonhand
        self.amountmadepercraft = amountmadepercraft
        self.amountneeded = amountneeded


class Node(basicNode):
    parent = None
    children: dict = {}
    instancekey: int = 0
    instances: int = 0
    generation: int = 0

    def __init__(self, ingredient: str = '', parent=None, amountonhand: int = 0, amountmadepercraft: int = 1, amountneeded: int = 1) -> None:
        """_summary_

        Args:
            ingredient (str, optional): _description_. Defaults to ''.
            parent (_type_, optional): _description_. Defaults to None.
            amountonhand (int, optional): _description_. Defaults to 0.
            amountmadepercraft (int, optional): _description_. Defaults to 1.
            amountneeded (int, optional): _description_. Defaults to 1.
        """
        super().__init__(ingredient, amountonhand, amountmadepercraft, amountneeded)
        Node.instancekey = Node.instances
        self.children = {}
        Node.instances += 1
        self.parent = parent
        if self.parent is not None and isinstance(self.parent, Node):
            self.generation = self.parent.generation + 1
            self.children.update({self.parent.instancekey: self.parent})
            self.parent.children.update({self.instancekey: self})
        elif self.parent is None and not isinstance(self.parent, Node):
            self.generation = 0
        else:
            raise TypeError('parent must be of type Node or None')
        



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
    red: float = ((cur.amountmadepercraft/cur.amountneeded)** -1)*cur.amountresulted
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

if __name__ == '__main__':
    # prompt ingredient tree
    print('What is the name of the item you want to create')
    testvalue: Node = populate(Node(input()))
    print('terminating process')
# end main