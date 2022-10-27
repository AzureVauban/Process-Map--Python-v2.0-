"""
Rework for Python 3.11.0
- Merge into development branches once completed
- save working stabe backup of solution.py before merging into development branches into the Stable branch
"""
import random
FIELDNAMES: list = [ # list of field names for the csv output file
    'Tree_Key',
    'Ingredient',
    'Ingredient_Alias',
    'Parent_of_Ingredient',
    'Amount_on_Hand',
    'Amount_Made_Per_Craft',
    'Amount_Needed_Per_Craft',
    'Generation'
]
CSVFILENAME : str = 'output.csv' # output of  csv file name
GLOBALNODEDICT : dict = {} # use for searching for nodes in populate method

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
    queueamountresulted: dict = {} # key, ingredient, value integer amount of resulted number from previous Node
    def __init__(self,ingredient : str = '',amountonhand : int = 0,amountmadepercraft : int = 0, amountneeded : int = 0) -> None:
        self.ingredient = ingredient
        self.amountonhand = amountonhand
        self.amountmadepercraft = amountmadepercraft
        self.amountneeded = amountneeded
class Node():
    pass
if __name__ == '__main__':
    print(generatename()) # test generatename function
