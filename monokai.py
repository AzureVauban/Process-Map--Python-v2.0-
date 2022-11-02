"""
Restructured main.py script
Changes:
- inputting and outputting ingredient trees into csv file
- the ability to search for ingredients for ease of typing out the ingredient tree
- user can take an ingredient tree from a csv file and use it as a template for a new recipe
= allow for usage of basic arithmetic operators when prompted to input a number (still in progress)
"""
import sys
import math

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
    class for storing simple data about an item such as its name and how much is needed to create
    its parent
    """
    ingredient: str = ''
    aliasingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountofparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, ingredient: str = '', amountonhand: int = -1, amountofparentmadepercraft: int = -1, amountneeded: int = -1) -> None:
        """
        stores information about basic ingredients

        Args:
            ingredient (str, optional): _description_. Defaults to ''.
            amountonhand (int, optional): _description_. Defaults to -1.
            amountofparentmadepercraft (int, optional): _description_. Defaults to -1.
            amountneeded (int, optional): _description_. Defaults to -1.
        """
        self.amountonhand = amountonhand
        self.amountofparentmadepercraft = amountofparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.aliasingredient = self.ingredient
        self.amountresulted = 0


class Node(MonokaiNode):
    """
    stores identifiable features of an item, such as the parent and children
    instances
    Args:
        NobeB (class): parent class of item
    """
    parent = None
    children: dict = {}
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
    # generate treekey
    # @note create a method that will generate a treekey for a node
    # end def

    # @ private method
    # prompt integer
    # @note prompts the user to input an integer
    # end def

    # create pandas csv row
    # @note create a pandas csv row dict
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

    # arithmetic method
    # @note set the amount resulted of each member of the tree to the result
    # of the arithmetic operation
    # end def

    def recursive_arithmetic(self) -> int:
        """_summary_

        Returns:
            int: _description_
        """
        # reverse artithmetic method
        # @note set the amount on hand of each member of the tree to the
        # result of the arithmetic operation
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
        self.amountresulted = desiredamount
        red: float = ((self.amountofparentmadepercraft/self.amountneeded)
                      ** -1)*self.amountresulted
        green: float = round(math.ceil(red))
        self.amountonhand = int(max(red, green))
        traceback: bool = green > red
        if traceback:  # go back through the higher up nodes and increase the amount on hand by 1
            temp: Node = self
            while temp.parent is not None:
                temp = temp.parent
                temp.amountonhand += 1
        # continue method reselfsively
        if len(self.children) > 0:
            for childnode in self.children.items():
                if not isinstance(childnode[1], Node):
                    raise TypeError('child is not an instance of', Node)
                recursive_recursive_arithmetic(childnode[1], self.amountonhand)
        return self.amountonhand


def populate(monokai: Node) -> Node:
    return monokai


def subpopulate(noctis: dict) -> Node:
    return Node('noctis')
