"""
Rework for Python 3.11.0
- Merge into development branches once completed
- save working stabe backup of solution.py before merging into development branches into the Stable branch
"""

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

if __name__ =
