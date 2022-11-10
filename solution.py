"""Reformat of main.py
- functional programming
"""

from enum import Enum
import math
import sys


class ProgramState(Enum):
    """
    tentative docstring description
    """
    MODE_A = 0  # recursive arithmetic (amountresulted)
    MODE_B = 1  # inverse recursive arithmetic (amountonhand)


MODE: ProgramState = ProgramState.MODE_A


class NodeB:  # pylint: disable=R0903
    """
    tentative docstring description
    """
    ingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}
    aliasingredient: str = ''

    def __init__(self, ingredient: str = '',
                 amountonhand: int = 0,
                 amountparentmadepercraft: int = 1,
                 amountneeded: int = 1) -> None:
        """
        tentative docstring description
        """
        self.amountonhand = amountonhand
        self.amountparentmadepercraft = amountparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.amountresulted = 0
        self.aliasingredient = ingredient.replace(' ', '_')
    # end def
# end def


class Node(NodeB):  # pylint: disable=R0913
    """
    tentative docstring description
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0

    def __init__(self, ingredient: str = '',  # pylint: disable=R0913
                 parent=None,
                 amountonhand: int = 0,
                 amountparentmadepercraft: int = 1,
                 amountneeded: int = 1) -> None:
        super().__init__(ingredient,
                         amountonhand,
                         amountparentmadepercraft,
                         amountneeded)
        # self.treekey = treekey
        self.instancekey = Node.instances
        self.children = {}
        self.parent = parent
        if self.parent is not None:
            self.generation = self.parent.generation + 1
            self.parent.children.update({self.instancekey: self})
#            self.treekey = self.parent.treekey
        else:
            self.generation = 0
#            if self.treekey == '':
#                self.treekey = self.generate_treekey()
        Node.instances += 1
    # end def

    def recursivearithmetic(self) -> int:
        """
        tentative docstring description
        """
        # check and set minimum resulted if queue is not empty
        tentativeinteger: int = sys.maxsize
        if len(self.queueamountresulted) == 0:
            tentativeinteger = 0
        else:
            for myinteger in self.queueamountresulted.items():
                if myinteger[1] < tentativeinteger:
                    tentativeinteger = myinteger[1]
        red = (self.amountparentmadepercraft / self.amountneeded)
        blue = (red*self.amountonhand) + (red*tentativeinteger)
        blue = round(math.floor(blue))
        self.amountresulted = blue
        # recursively call the method
        if self.parent is not None:
            self.parent.queueamountresulted.update(
                {self.ingredient: self.amountresulted})
            self.parent.recursivearithmetic()
        return self.amountresulted
    # end def
# end def


def head(node: Node) -> Node:
    """
    traverse to the parent most Node

    Args:
        node (Node): starting Node

    Returns:
        Node: parent most Node of the starting Node
    """
    while node.parent is not None:
        node = node.parent
    return node
# end def


def trail(node: Node):
    """
    print the ingredient trail leading up to the parent most Node

    Args:
        node (Node): starting Node
    """
    print('TRAIL: ', end='')
    while True:
        if node.parent is not None:
            print(node.ingredient, '-> ', end='')
            node = node.parent
        else:
            print(node.ingredient)
            break
# end def


def outputingredients(node: Node):
    """
    print the subingredients of the parameter Node

    Args:
        node (Node): parent node, the node to print the subingredients of
    """
    subingredients: list = []
    for subnode in node.children.items():
        subingredients.append(subnode[1].ingredient)
    print('+ These ingredients are already in the tree:\n')
    # output the ingredients
    for index, ingredient in enumerate(subingredients):
        print(f'{index+1}. {ingredient}')
    print('')
# end def


def search(node: Node, ingredient: str, results: list) -> list:
    """
    recursively search through the tree to find nodes with the same
    ingredient

    Args:
        node (Node): parent node, parse through its children recursively to
        update the search results
        ingredient (str): the name of the item you are searching for
        results (list): nodes that have the same ingredient as the parameter

    Returns:
        list: a list of nodes that have the same ingredient as the parameter
    """
    # if node is a subnode and the ingredient matches, update the list
    if node.parent is not None and node.ingredient == ingredient:
        for subnode in node.children.items():
            results.append(subnode[1])
    # recrusively keep searching for nodes
    for subnode in node.children.items():
        search(subnode[1], ingredient, results)
    return results
# end def


def clone(node: Node) -> Node:
    """
    return a clone of the node

    Args:
        node (Node): node to clone from

    Returns:
        Node: a clone of the node which is a node instance with the same data
        but on a differing memory address
    """
    return node
# end def


def subpopulate(node: Node, ingredient: str) -> Node:
    """
    create a subnode and link it to the parent node

    Args:
        node (Node): parent Node to link back to

    Returns:
        Node: new subnode to link back to the parent Node
    """
    # create a list of subnodes that have the same ingredient as the parameter
    # if the list is empty return a defaultly created new node Node
    parseresults: list = search(node, ingredient, [])
    for subnode in parseresults:
        if not isinstance(subnode, Node):
            raise TypeError('item in the list is not an instance of', Node)
    if len(parseresults) == 0:
        return Node(ingredient, node)
    # else, prompt the user to create a linkable clone of the new node
    for index, subnode in enumerate(parseresults):
        # output the choices of subnodes:
        # parent ingredient, amountneeded, amountmadepereachcraft
        print(index+1, str('. ' + subnode.parent.ingredient
                           + '|' + str(subnode.amountneeded)
                           + '|' + str(subnode.amountparentmadepercraft)))
    userchoice: int = int(input('Choose a subnode to clone: '))
    userchoice -= 1
    # if the user chooses to create a new node, return a clone subnode
    if userchoice < 0 or userchoice > len(parseresults)-1:
        # if the user did not input a valid index
        # if not return the defaultly created new node
        return Node(ingredient, node)
    return clone(parseresults[userchoice])
# end def


def populate(node: Node) -> Node:
    """create a tree of Nodes

    Args:
        node (Node): parent the subnodes will be linked to

    Returns:
        Node: the head of the ingredient tree
    """
    # output the ingredient trail if there is a parent Node
    if node.parent is not None:
        trail(node)
    # prompt the user to ingredient tree
    userinputs: list = []  # list of tuples (string, bool)
    # append subnode ingredients to the list if there are any
    for subnode in node.children.items():
        userinputs.append((subnode[1].ingredient, True))
    # prompt the user for ingredients
    print('What ingredients do you have need to create',
          node.ingredient, end=':\n')
    # if there are subnodes, prompt the user to select from the list
    if len(node.children) > 0:
        outputingredients(node)
    while True:
        # create ingredients blacklist
        ingredientblacklist: list = []
        for ingredient in userinputs:
            ingredientblacklist.append(ingredient[0])
        # prompt the user for an ingredient
        myinput: str = input('').strip()
        # check to see if the user input is the same as the parent or head Node
        if myinput in [head(node).ingredient, node.ingredient]:
            print('Invalid input, we are trying to make that item!')
        # if the length of the user input is 0, break the loop
        elif myinput in ingredientblacklist:
            print('Invalid input, duplicate inputs!')
        # if the input is empty, break out of the loop
        elif len(myinput) == 0:
            break
        # append to the user inputs list if all the checks pass
        else:
            # if the condition is met, append the input to the list
            userinputs.append((myinput, False))
    # create subnodes for each ingredient using the subpopulate method
    for ingredient in userinputs:
        # if ingredient[1] is False, the ingredient is not already in the tree
        if not ingredient[1]:
            subpopulate(node, ingredient[0])
    # recrusively continue to populate the tree
    for subnode in node.children.items():
        populate(subnode[1])
    # if the program Mode is A and the length of the children Nodes are 0
    # @note call recursive arithmetic method here
    if MODE == ProgramState.MODE_A and len(node.children) == 0:
        # call the arithmetic method
        node.recursivearithmetic()
    # return the head of the ingredient tree
    return head(node)
# end def


if __name__ == '__main__':
    industrial_battery: Node = Node('industrial battery', None)
    protocite_bar: Node = Node('protocite bar', industrial_battery, 0, 1, 5)
    protocite: Node = Node('protocite', protocite_bar, 0, 1, 2)
    battery: Node = Node('battery', industrial_battery, 0, 1, 2)
    pixels: Node = Node('pixels', battery, 0, 1, 2500)
    quantum_processor: Node = Node('quantum processor', industrial_battery)
    silicon_board: Node = Node('silicon board', quantum_processor, 0, 1, 4)
    protocite_bar2: Node = Node('protocite bar', quantum_processor, 0, 1, 2)
    protocite2: Node = Node('protocite', protocite_bar2, 0, 1, 2)
    thorium_rod: Node = Node('thorium rod', industrial_battery, 0, 1, 5)
    thorium_ore: Node = Node('thorium ore', thorium_rod, 0, 1, 2)
    populate(head(thorium_ore))
    print('terminating program')
# end main
