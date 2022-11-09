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
                 parent = None,
                 amountonhand: int = 0, 
                 amountparentmadepercraft: int = 1, 
                 amountneeded: int = 1) -> None:
        super().__init__(ingredient,
                         amountonhand, 
                         amountparentmadepercraft, 
                         amountneeded)
        self.parent = parent
        