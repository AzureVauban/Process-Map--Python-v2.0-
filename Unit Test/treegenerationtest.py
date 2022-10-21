# create a class for randomly generated Nodes
import random
import unittest

from main import Node


def generatename(lengthlimit: int = random.randint(10, 20)) -> str:
    """_summary_

    Returns:
        str: _description_
    """
    # create a random name as a string
    yuggoth: str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    mocknodename: str = ''
    for _ in range(random.randint(6, lengthlimit)):
        mocknodename += random.choice(yuggoth)
    return mocknodename

    def __init__(self, name: str, parent=None, amountonhand: int = 0, amountneeded: int = 1, amountmadepercraft: int = 1) -> None:
        """_summary_

        Args:
            name (str): _description_
            parent (_type_, optional): _description_. Defaults to None.
            amountonhand (int, optional): _description_. Defaults to 0.
            amountneeded (int, optional): _description_. Defaults to 1.
            amountmadepercraft (int, optional): _description_. Defaults to 1.
        """
        self.name = name
        self.parent = parent
        self.amountonhand = amountonhand
        self.amountneeded = amountneeded
        self.amountmadepercraft = amountmadepercraft


class NodeTree:
    """`create a randomly generated ingredient tree of Nodes"""
    headnode: Node
    population: int

    def verifyuniqueness(self, name: str, leaf: Node) -> bool:
        # verify that a given string name is unique in the tree
        if name == self.leaf.name:
            return False
        else:
            for leaves in leaf.children.items():
                self.verifyuniqueness(name, leaves[1])
        return True  # ! replace this line of code with a recursive method that returns True if the name is unique

    def generateTree(self, population: int = 100, head: Node = Node(generatename(), None, 0, 1, 1)) -> Node:
        # ! replace this line of code with augment Node instances as the return value
        return head

    def updatepopulation(self, leaf: Node, count: int = 1) -> int:
        return count  # ! replace this line of code with a recursive method that returns the number of nodes in the tree

    def generate_rainforest(self, numberoftrees: int = random.randint(1, 10)) -> dict:
        NodeForest: dict = {}
        for _ in range(numberoftrees):
            NodeForest.update({self.updatepopulation(
                self.generateTree()): self.generateTree()})
        return NodeForest

    def __init__(self, population_limit: int = random.randint(1, 50)) -> None:
        self.headnode = self.generateTree(population_limit)
        self.population = self.updatepopulation(self.headnode)
        if self.population > 1:
            print('generated a tree with', self.population,
                  'nodes called', self.headnode.name)
        else:
            print('generated a tree with', self.population,
                  'node called', self.headnode.name)


class testgeneration(unittest.TestCase):
    def testuniqueness(self):
        pass
