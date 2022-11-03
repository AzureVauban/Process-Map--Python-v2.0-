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
  
  # red vs blue, boolean comparison for checking
  # red vs green, boolean comparison for program flow
"""
import sys
import math
import random
from enum import Enum

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


class ProgramMode(Enum):
    """change the docstring of this method
    """
    AMOUNTONHAND = 0
    AMOUNTRESULTED = 1


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

    def __init__(self, ingredient: str = '', amountonhand: int = 0, amountofparentmadepercraft: int = 1, amountneeded: int = 1) -> None:  # noqa: E501 #pylint: disable=line-too-long
        super().__init__(ingredient, amountonhand, amountofparentmadepercraft, amountneeded)  # noqa: E501 #pylint: disable=line-too-long
        print('test method for', ingredient)
        self.__promptinput_int()

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

    def checkuniqueness(self, base: None, ingredient: str = '') -> bool:
        """change the docstring of this method
        """
        # @todo do alot of testing before using this method
        # check if there is are any other nodes in the tree with the same
        # ingredient name as the current node
        if not isinstance(base, Node):
            raise TypeError('base is not an instance of', Node)
        if self is not base and self.ingredient == ingredient:
            return False
        for subnode in self.children.items():
            if not isinstance(subnode[1], Node):
                raise TypeError('child is not an instance of', Node)
            if not subnode[1].checkuniqueness(base, ingredient):
                return False
            return True
        return True
    # end def

    def __promptinput_int(self) -> int:
        """change the docstring of this method
        """
        # private method for prompting the user to input an integer
        # @note used in the __setamounts method
        while True:
            userinput: str = input('').strip()
            if not isdigit(userinput):
                print('please input an integer')
                continue
            else:
                
        return 0
    # end def

    def __setamounts(self):
        """change the docstring of this method
        """
        # method for setting the amount variables of each node instance
        # @note this method is called when the node is created
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
# end def


if __name__ == '__main__':
    test = Node('apple')
    print('terminating program')
