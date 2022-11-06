"""
Restructured main.py script
Changes:
- inputting and outputting ingredient trees into csv file
- the ability to search for ingredients for ease of typing out the ingredient
  tree
- user can take an ingredient tree from a csv file and use it as a template
   for a new recipe
= allow for usage of basic arithmetic operators when prompted to input a
  number (still in progress)
  # red vs blue, boolean comparison for checking
  # red vs green, boolean comparison for program flow
"""
import sys
import math
import random
from enum import Enum

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


class ProgramMode(Enum):
    """change the docstring of this method
    """
    AMOUNTONHAND = 0
    AMOUNTRESULTED = 1


# end def
Mode: Enum = ProgramMode.AMOUNTONHAND


class MonokaiNode:
    """change the docstring of this method
    """
    ingredient: str = ''
    aliasingredient: str = ''
    amountonhand: int = 0
    amountneeded: int = 0
    amountofparentmadepercraft: int = 0
    amountresulted: int = 0
    queueamountresulted: dict = {}

    def __init__(self, ingredient: str = '', amountonhand: int = -1, amountofparentmadepercraft: int = -1, amountneeded: int = -1) -> None:  # noqa: E501 #pylint: disable=line-too-long
        """change the docstring of this method
        """
        self.amountonhand = amountonhand
        self.amountofparentmadepercraft = amountofparentmadepercraft
        self.amountneeded = amountneeded
        self.queueamountresulted = {}
        self.ingredient = ingredient
        self.aliasingredient = self.ingredient
        self.amountresulted = 0
# end def


class Node(MonokaiNode):
    """change the docstring of this method
    """
    parent = None
    children: dict = {}
    aliasingredient: str = ''
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    askmadepercraft: bool = False
    # this is unique identifer for an ingredient tree when its outputted into
    # a csv file
    treekey: str = ''
    # a dictionary of all the nodes declared during runtime
    search: dict = {}

    def __init__(self, ingredient: str = '', parent=None, amountonhand: int = 0, amountofparentmadepercraft: int = 1, amountneeded: int = 1, askmadepercraft: bool = True) -> None:  # noqa: E501 #pylint: disable=line-too-long
        """change the docstring of this method
        """
        super().__init__(ingredient, amountonhand, amountofparentmadepercraft, amountneeded)  # noqa: E501 #pylint: disable=line-too-long
        self.children = {}
        self.instancekey = Node.instances
        if not isinstance(parent, Node) and parent is not None:
            raise TypeError('parent is not an instance of', Node)
        self.askmadepercraft = askmadepercraft  # noqa: E501 #pylint: disable=line-too-long
        if parent is not None:
            self.parent = parent
            self.parent.children.update({self.instancekey: self})
            self.generation = self.parent.generation + 1
            self.treekey = self.parent.treekey
            # the bool above is used to determine if the amountmadepercraft
            # should be set by prompt or by the constructor
        else:
            self.generation = 0
            self.treekey = self.generate_treekey()
        if __name__ == '__main__' and self.parent is not None:
            self.__setamounts()
        Node.instances += 1

    @classmethod
    def generate_treekey(cls, length: int = random.randint(5, 20)) -> str:
        """change the docstring of this method
        """
        # generate treekey
        # @note create a method that will generate a treekey for a node
        cls.treekey = ''
        for _ in range(0, length):
            cls.treekey += random.choice(
                '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')  # noqa: E501 #pylint: disable=line-too-long
        return cls.treekey
    # end def

    def checkuniqueness(self, base: None, ingredient: str = '') -> bool:
        """change the docstring of this method
        """
        # @todo do alot of testing before using this method
        # check if there is are any other nodes in the tree with the same
        # ingredient name as the current node
        if not isinstance(base, Node):
            raise TypeError('base is not an instance of', Node)
        if self is not base and self.ingredient == ingredient:
            return False
        for subnode in self.children.items():
            if not isinstance(subnode[1], Node):
                raise TypeError('child is not an instance of', Node)
            if not subnode[1].checkuniqueness(base, ingredient):
                return False
            return True
        return True
    # end def

    def __promptinput_int(self) -> int:
        """change the docstring of this method
        """
        # private method for prompting the user to input an integer
        # @note used in the __setamounts method
        while True:
            userinput: str = input('').strip()
            if not userinput.isdigit():
                print('please input an integer')
            else:
                return int(userinput)
    # end def

    def __setamounts(self):
        """change the docstring of this method
        """
        # method for setting the amount variables of each node instance
        # @note this method is called when the node is created
        print('What is the amount of', self.ingredient, 'on hand you have?')
        # only ask if the program state is AMOUNTONHAND
        self.amountonhand = self.__promptinput_int()
        if self.parent is not None:
            print('What is the amount of', self.ingredient,
                  'needed to create', self.parent.ingredient, 'once?')
            self.amountneeded = self.__promptinput_int()

        if self.askmadepercraft and self.parent is not None:
            # if a leading sibiling has  already asked this question, then
            # skip it
            print('What is the amount of parent ingredient',
                  self.parent.ingredient, 'made per craft?')
            self.amountofparentmadepercraft = self.__promptinput_int()
    # end def

    def recursive_arithmetic(self) -> int:
        """change the docstring of this method
        """
        # arithmetic method
        # @note set the amount resulted of each node
        tentativeinteger: int = sys.maxsize
        if len(self.queueamountresulted) == 0:
            tentativeinteger = 0
        else:
            for myinteger in self.queueamountresulted.items():
                if myinteger[1] < tentativeinteger:
                    tentativeinteger = myinteger[1]
        red = (self.askmadepercraft / self.amountneeded)
        blue = (red*self.amountonhand) + (red*tentativeinteger)
        blue = round(math.floor(blue))
        self.amountresulted = blue
        # reselfsively call the method
        if self.parent is not None:
            self.parent.queueamountresulted.update(
                {self.ingredient: self.amountresulted})
            self.parent.recursive_arithmetic()
        return self.amountresulted
    # end def

    def recursive_recursive_arithmetic(self, desiredamount: int) -> int:
        """change the docstring of this method
        """
        # reverse artithmetic method
        # @note set the amount on hand of each node
        self.amountresulted = desiredamount
        red: float = ((self.askmadepercraft/self.amountneeded)
                      ** -1)*self.amountresulted
        green: float = round(math.ceil(red))
        self.amountonhand = int(max(red, green))
        traceback: bool = green > red
        if traceback:
            temp: Node = self
            while temp.parent is not None:
                temp = temp.parent
                temp.amountonhand += 1
        # recursively call the method on each child
        if len(self.children) > 0:
            for childnode in self.children.items():
                if not isinstance(childnode[1], Node):
                    raise TypeError('child is not an instance of', Node)
                self.recursive_recursive_arithmetic(self.amountonhand)
        return self.amountonhand
    # end def

    @classmethod
    def update_search_dict(cls, node=None) -> dict:
        """change the docstring of this method
        """
        # the stores the treekey as a key, and stores a list of tuples
        if not isinstance(node, Node):
            raise TypeError('node is not an instance of', Node)
        # update the dict with the treekey as a key, and the node as a value
        cls.search.update({node.instancekey: node})
        # return the modified dict
        return cls.search

    @classmethod
    def clear_search_dict(cls) -> dict:
        """change the docstring of this method
        """
        # clears the search dict
        cls.search = {}
        return cls.search

    @classmethod
    def search_for_ingredient(cls, ingredient: str) -> dict:
        """change the docstring of this method
        """
        results: dict = {}
        for node in cls.search.items():
            if node[1].ingredient == ingredient:
                results.update({node[0]: node[1]})
        if len(results) == 0:
            return {-1: None}
        return results

    def locateendpoints(self, foundendpoints: list) -> list:
        """change the docstring of this method
        """
        if len(self.children.items()) == 0:
            foundendpoints.append(self)
        else:
            for node in self.children.items():
                if not isinstance(node[1], Node):
                    raise TypeError('node is not an instance of', Node)
                node[1].locateendpoints(foundendpoints)
        return foundendpoints
# end def


def head(node: Node) -> Node:
    """change the docstring of this method
    """
    # @note get the top node of a tree
    while node.parent is not None:
        node = node.parent
    return node
# end def


def populate(node: Node) -> Node:
    """change the docstring of this method
    """
    inputqueue: dict = {}
    checkstring: str = node.ingredient
    # output ingredient trail
    if node.parent is not None:
        tempinstance: Node = node
        print('TRAIL: ', end='')
        while True:
            if tempinstance.parent is not None:
                print(tempinstance.ingredient, '-> ', end='')
                tempinstance = tempinstance.parent
            else:
                print(tempinstance.ingredient)
                break
        checkstring = tempinstance.ingredient
    # prompt user to input ingredients
    print('What ingredients do you need to create', node.ingredient, end=':\n')
    while True:
        myinput = input('')
        myinput = myinput.strip()
        # input validation
        duplicated: bool = False
        if len(inputqueue) > 0:
            for word in inputqueue.items():
                duplicated = word[1] == checkstring
                if duplicated:
                    break
        if duplicated:
            print('You already typed that in')
        elif myinput == checkstring:
            print('Invalid input, we are trying to make that item!')
        elif myinput == node.ingredient:
            print('You cannot type that in')
        elif len(myinput) == 0:
            break
        else:
            inputqueue.update({len(inputqueue): myinput})
    # create new child instances
    tempbool: bool = True
    amountresulted: int = 1
    for ingredient in inputqueue.items():  # @todo test this out
        _: Node = subpopulate(ingredient[1], node, tempbool, amountresulted)
        if tempbool:
            tempbool = False
            amountresulted = _.amountresulted
    # input current argument node in search container
    if node.parent is not None:  # @todo test this out
        node.update_search_dict(node)
    # continue method runtime
    for child in node.children.items():
        if isinstance(child[1], Node):
            populate(child[1])
        else:
            raise TypeError('child is not an instance of', Node)
    return head(node)
# end def


def subpopulate(ingredient: str, node: Node, promptamountmade: bool, amount_resulted: int = 1) -> Node:  # noqa: E501 #pylint: disable=line-too-long
    """change the docstring of this method
    """
    # if search method returns {-1:None}, create a new node
    queryresults: dict = node.search_for_ingredient(ingredient)
    if queryresults == {-1: None}:
        return Node(ingredient, node, askmadepercraft=promptamountmade,
                    amountofparentmadepercraft=amount_resulted)
    userchoices: list = []
    for itemnode in queryresults.items():
        userchoices.append(itemnode[1])
    if len(userchoices) == 1:
        print('do you want to use a copy of', userchoices[0].ingredient, 'back in the tree?')  # noqa: E501 #pylint: disable=line-too-long
        # !return userchoices[0]
        return Node(ingredient, node, askmadepercraft=promptamountmade,
                    amountofparentmadepercraft=amount_resulted)
    elif len(userchoices) == 0:
        raise ValueError('userchoices is empty')
    else:
        print('Do you want to use any of these nodes back into the tree', end=':\n')  # noqa: E501 #pylint: disable=line-too-long
        for item in userchoices:
            print(item.parent.ingredient, ':',
                  item.amountmadepercraft, '|', item.amountneeded)
        # !return random.choice(userchoices)
        return Node(ingredient, node, askmadepercraft=promptamountmade,
                    amountofparentmadepercraft=amount_resulted)


if __name__ == '__main__':
    Node.search = {}
    # prompt user what mode do they want to run the program in
    # prompt user to create an ingredient tree
    desireditem: str = ''
    while True:
        print('What item do you want to make?')
        desireditem = input('').strip()
        if len(desireditem) == 0:
            print('Invalid input')
        else:
            break
    headnode: Node = populate(Node(desireditem, None))
    # perform calculations
    if Mode == ProgramMode.AMOUNTONHAND:
        userdesiredamount: int = random.randint(1, 1000)
        print('solving for the amount on hand')  # !remove this later
        for monokainode in headnode.locateendpoints([]):
            if not isinstance(monokainode, Node):
                raise TypeError('pynode is not an instance of', Node)
            monokainode.recursive_recursive_arithmetic(userdesiredamount)
    else:
        print('solving for the amount on hand')  # !remove this later
    print('terminating program')
