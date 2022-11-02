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
CSVFILENAME : str = 'solution_ingredient_trees.csv'
PROGRAMMODETYPE: int = 0 #! turn this into an enum

class NodeB:
    """
    class for storing simple data about an item such as its name and how much is needed to create
    its parent
    """
    ingredient: str = ''
    aliasingredient: str = ''
    