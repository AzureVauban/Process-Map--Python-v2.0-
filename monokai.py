"""
Restructured main.py script
Changes:
- inputting and outputting ingredient trees into csv file
- the ability to search for ingredients for ease of typing out the ingredient tree
- user can take an ingredient tree from a csv file and use it as a template for a new recipe
= allow for usage of basic arithmetic operators when prompted to input a number (still in progress)
"""

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
    ismain_promptinputbool: bool = True
    # methods
    # @ classmethod
    # generate treekey
    #@note create a method that will generate a treekey for a node
    # end def

    # @ private method
    # prompt integer
    #@note prompts the user to input an integer
    # end def

    # create pandas csv row
    # end def

    # create pandas csv rows
    # end def

    # return head
    # end def

    # return tree endpoints
    # end def