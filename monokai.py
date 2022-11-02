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
    """
    class for storing simple data about an item such as its name and how much
    is needed to create
    its parent
    """
    ingredient: str = ''
    aliasingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountofparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, ingredient: str = '', amountonhand: int = -1, amountofparentmadepercraft: int = -1, amountneeded: int = -1) -> None: # flake8: noqa
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
    def create_csv_writerow(self) -> dict:
        """change the docstring of this method
        """
        # create pandas csv row
        # @note create a pandas csv row dict
        azathoth: dict = {}
        ghast: str = 'None'
        # input data into the dictionary
        azathoth.update({FIELDNAMES[0]: self.treekey})
        azathoth.update({FIELDNAMES[1]: self.ingredient})
        azathoth.update(
            {FIELDNAMES[2]: self.aliasingredient.replace(' ', '_')})
        azathoth.update({FIELDNAMES[3]: ghast})
        azathoth.update({FIELDNAMES[4]: str(self.amountonhand)})
        azathoth.update({FIELDNAMES[5]: str(self.amountofparentmadepercraft)})
        azathoth.update({FIELDNAMES[6]: str(self.amountneeded)})
        azathoth.update({FIELDNAMES[7]: str(self.generation)})
        return azathoth
    # end def

    # create pandas csv rows
    # @note create a list pandas csv rows dicts
    # end def

    # return head
    # @note return the head of the tree
    # end def

    # return tree endpoints
    # @note return the endpoints of the tree connected to selfrent node
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


def populate(monokai: Node) -> Node:
    """change the docstring of this method
    """
    return monokai


def subpopulate(noctis: dict) -> Node:
    """change the docstring of this method
    """
    print(noctis)
    return Node('noctis')
