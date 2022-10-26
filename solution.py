"""
Reorganize main.py
"""
class baseNode:
    ingredient : str
    ingredient_alias : str 
    amountonhand : int = 0
    amountneeded : int = 0
    amountmadepercraft : int = 0
    def __init__(self) -> None:
        pass
class Node(baseNode):
    instances : int
    instancekey : int
class TreeNode():
    population : int
    canopynode : Node
    def __init__(self,population : int) -> None: