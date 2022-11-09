"""Reformat of main.py
- functional programming
"""


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


class Node(NodeB):
    """
    tentative docstring description
    """
    parent = None
    children: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0

    def __init__(self, ingredient: str = '',
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
    userinputs : list = []
    # append subnode ingredients to the list if there are any
    for subnode in node.children.items():
        userinputs.append(subnode[1].ingredient)
    # recrusively create the tree
    for subnode in node.children.items():
        populate(subnode[1])
    # return the head of the ingredient tree
    return head(node)
# end def


if __name__ == '__main__':
    industrial_battery: Node = Node('industrial battery', None)
    protocite_bar: Node = Node('protocite bar', industrial_battery, 0, 1, 5)
    protocite: Node = Node('protocite', protocite_bar, 0, 1, 2)
    battery: Node = Node('battery', industrial_battery, 0, 1, 2)
    pixels: Node = Node('pixels', battery, 0, 1, 2500)
    quantum_processor: Node = Node(
        'quantum processor', industrial_battery, 0, 1, 1)
    silicon_board: Node = Node('silicon board', quantum_processor, 0, 1, 4)
    protocite_bar2: Node = Node('protocite bar', quantum_processor, 0, 1, 2)
    protocite2: Node = Node('protocite', protocite_bar2, 0, 1, 2)
    thorium_rod: Node = Node('thorium rod', industrial_battery, 0, 1, 5)
    thorium_ore: Node = Node('thorium ore', thorium_rod, 0, 1, 2)
    trail(thorium_ore)
# end main
