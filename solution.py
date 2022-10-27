"""
Rework for Python 3.11.0
- Merge into development branches once completed
- save working stabe backup of solution.py before merging into development branches into the Stable branch
"""
import random
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
        



def populate(node: Node):
    """_summary_

    Args:
        node (Node): current endpount node of the ingredient tree

    Returns:
        Node: head of tree
    """
    print('What do you need to create', node.ingredient, end='?\n')
    return node 


if __name__ == '__main__':
    # prompt ingredient tree
    print('What is the name of the item you want to create')
    testvalue: Node = populate(Node(input()))
    print('terminating process')
# end main
