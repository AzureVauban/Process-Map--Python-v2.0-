"""
Restructured main.py script
Changes:
- inputting and outputting ingredient trees into csv file
- the ability to search for ingredients for ease of typing out the ingredient
  tree
- user can take an ingredient tree from a csv file and use it as a template
   for a new recipe
= allow for usage of basic arithmetic operators when prompted to input a
  number (still in progress)
"""
import sys
import math
import random

FIELDNAMES: list = [
    'Tree_Key',
    'Ingredient',
    'Ingredient_Alias',
    'Parent_of_Ingredient',
    'Amount_on_Hand',
    'Amount_Of_Parent_Made_Per_Craft',
    'Amount_Needed_Per_Craft',
    'Generation'
]
CSVFILENAME: str = 'solution_ingredient_trees.csv'
PROGRAMMODETYPE: int = 0  # ! turn this into an enum


class MonokaiNode:
    """change the docstring of this method
    """
    ingredient: str = ''
    aliasingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountofparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, ingredient: str = '', amountonhand: int = -1, amountofparentmadepercraft: int = -1, amountneeded: int = -1) -> None:  # noqa: E501 #pylint: disable=line-too-long
        """change the docstring of this method
        """
        self.amountonhand = amountonhand
        self.amountofparentmadepercraft = amountofparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.aliasingredient = self.ingredient
        self.amountresulted = 0


class Node(MonokaiNode):
    """change the docstring of this method
    """
    parent = None
    children: dict = {}
    aliasingredient: str = ''
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    askmadepercraftquestion: bool = False
    # this is unique identifer for an ingredient tree when its outputted into
    # a csv file
    treekey: str = ''
    ismain_promptinputbool: bool = True
    # methods

    # @ classmethod
    @classmethod
    def generate_treekey(cls, length: int = random.randint(5, 20)) -> str:
        """change the docstring of this method
        """
        # generate treekey
        # @note create a method that will generate a treekey for a node
        cls.treekey = ''
        for _ in range(0, length):
            cls.treekey += random.choice(
                '0123456789abcdefghijklmnopqrstuvwxyz\
                    ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return cls.treekey
    # end def

    # @ private method
    # prompt integer
    # @note prompts the user to input an integer
    # end def
    def create_pandas_dataframerow(self) -> dict:
        """change the docstring of this method
        """
        # create pandas csv row
        # @note create a pandas csv row dict
        dictrow: dict = {}
        ghast: str = 'None'
        # input data into the dictionary
        dictrow.update({FIELDNAMES[0]: self.treekey})
        dictrow.update({FIELDNAMES[1]: self.ingredient})
        dictrow.update(
            {FIELDNAMES[2]: self.aliasingredient.replace(' ', '_')})
        dictrow.update({FIELDNAMES[3]: ghast})
        dictrow.update({FIELDNAMES[4]: str(self.amountonhand)})
        dictrow.update({FIELDNAMES[5]: str(self.amountofparentmadepercraft)})
        dictrow.update({FIELDNAMES[6]: str(self.amountneeded)})
        dictrow.update({FIELDNAMES[7]: str(self.generation)})
        return dictrow
    # end def

    def create_pandas_dataframerows(self, treerows: list) -> list:
        """change the docstring of this method
        """
        # create pandas csv rows
        # @note create a list pandas csv rows dicts
        treerows.insert(0, self.create_pandas_dataframerow())
        for child in self.children.items():
            if not isinstance(child[1], Node):
                raise TypeError('Child is not an instance of', Node)
            child[1].create_pandas_dataframerows(treerows)
        # make sure that the list is ordered correctly
        if not len(treerows) // 2 == 0:
            return treerows[::-1]
        return treerows
    # end def

    def head(self) -> None:
        """change the docstring of this method
        """
        # return head
        # @note return the head of the tree
    # end def

    def findendpoints(self, endpoints: dict, startfromhead: bool = False) -> dict:  # noqa: E501 #pylint: disable=line-too-long
        """change the docstring of this method
        """
        # return tree endpoints
        # @note return the endpoints of the tree connected to selfrent node
        if not startfromhead and self.parent is not None:
            self.findendpoints(endpoints, False)
        elif not startfromhead and self.parent is None:
            self.findendpoints(endpoints, True)
        elif startfromhead and len(self.children) == 0:
            endpoints.update({self.instancekey: self})
        else:
            for child in self.children.items():
                child[1].findendpoints(endpoints, True)
        return endpoints
    # end def

    def recursive_arithmetic(self) -> int:
        """change the docstring of this method
        """
        # arithmetic method
        # @note set the amount resulted of each node
        tentativeinteger: int = sys.maxsize
        if len(self.queueamountresulted) == 0:
            tentativeinteger = 0
        else:
            for myinteger in self.queueamountresulted.items():
                if myinteger[1] < tentativeinteger:
                    tentativeinteger = myinteger[1]
        red = (self.amountofparentmadepercraft / self.amountneeded)
        blue = (red*self.amountonhand) + (red*tentativeinteger)
        blue = round(math.floor(blue))
        self.amountresulted = blue
        # reselfsively call the method
        if self.parent is not None:
            self.parent.queueamountresulted.update(
                {self.ingredient: self.amountresulted})
            self.parent.recursive_arithmetic()
        return self.amountresulted
    # end def

    def recursive_recursive_arithmetic(self, desiredamount: int) -> int:
        """change the docstring of this method
        """
        # reverse artithmetic method
        # @note set the amount on hand of each node
        self.amountresulted = desiredamount
        red: float = ((self.amountofparentmadepercraft/self.amountneeded)
                      ** -1)*self.amountresulted
        green: float = round(math.ceil(red))
        self.amountonhand = int(max(red, green))
        traceback: bool = green > red
        if traceback:
            temp: Node = self
            while temp.parent is not None:
                temp = temp.parent
                temp.amountonhand += 1
        # recursively call the method on each child
        if len(self.children) > 0:
            for childnode in self.children.items():
                if not isinstance(childnode[1], Node):
                    raise TypeError('child is not an instance of', Node)
                self.recursive_recursive_arithmetic(self.amountonhand)
        return self.amountonhand
    # end def


def updatesearchdict(darcula: Node):
    """change the docstring of this method
    """
    # create a method to update a dictionary of all created nodes
    # @note the key is the treekey and the value is a list of all the nodes with
    # same tree key
    print(darcula)
# end def


def populate(monokai: Node) -> Node:
    """change the docstring of this method
    """
    inputqueue: dict = {}
    checkstring: str = monokai.ingredient
    # output ingredient trail
    if monokai.parent is not None:
        tempinstance: Node = monokai
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
    print('What ingredients do you need to create',
          monokai.ingredient, end=':\n')
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
        elif myinput == monokai.ingredient:
            print('You cannot type that in')
        elif len(myinput) == 0:
            break
        else:
            inputqueue.update({len(inputqueue): myinput})
    # create new child instances
    tempbool: bool = True
    searchdict: dict = {}
    for newnodename in inputqueue.items():
        # if search method doesn't return a dictionary with a key of -1 and
        # a value of None
        # prompt for copy
        # else
        # create new node
        # prompt if the user wants to copy an existing node if the search
        # query returns a dictionary
        # that deosn't have a key of -1 and a value of None
        # todo have someone test out the code
        # node declaration
        if subpopulate(searchdict, monokai, newnodename[1]) != {-1: None}:
            # @todo create a child node from the searchdict nodes
            pass
        else:  # if there was no Node found
            # @todo create a new node
            pass
        print(tempbool)
        tempbool = False
        # update the class searchdict
    # @audit-info make this update the class dict GLOBALNODEDICT.update
    # ({monokai.instancekey: cur})
    # @audit-info dict should keep the treekey as a key and a list of all the
    # nodes with that treekey as the item
    # continue method runtime
    for child in monokai.children.items():
        if isinstance(child[1], Node):
            populate(child[1])
        else:
            raise TypeError('child is not an instance of', Node)
    return monokai


def subpopulate(noctis: dict, lux: Node, lilac: str) -> dict:
    """change the docstring of this method
    """
    # return {-1:NONE} if there wasnt a node found in the search
    print(lilac)
    print(noctis, lux)
    return noctis
