# pylint:disable=C0302
"""
Reformat of main.py
"""

import math
import os
import random
import sys
import time
from enum import Enum

import pandas

# todo, update the csv functions to use a deque when needed


class ProgramState(Enum):
    """
    Enum for which mode the user selected during runtime
    """
    MODE_A = 0  # recursive arithmetic (amountresulted)
    MODE_B = 1  # inverse recursive arithmetic (amountonhand)


FILENAME: str = 'ingredient_trees.csv'
FIELDNAMES: list = [
    'Tree_Key',  # 74nry8keki',
    'Ingredient',  # Copper Wire
    'Ingredient_Alias',  # Copper_Wire2
    'Parent_of_Ingredient',  # Silicon Board
    'Amount_on_Hand',  # 0
    'Amount_Of_Parent_Made_Per_Craft',  # 9
    'Amount_Needed_Per_Craft',  # 0
    'Generation'  # 1
]


class Deque:
    """double ended queue"""
    class Node:  # pylint:disable=R0903
        """Node class for pillar data structure"""
        index: int
        data = None
        after = None
        before = None

        def __init__(self, before, data, after) -> None:
            self.before = before
            self.data = data
            self.after = after
            self.index = 0

    head: Node = None
    size: int = 0
    max_size: int = 0

    def __init__(self, max_size=None) -> None:
        self.head = None
        self.size = 0
        self.max_size = max_size

    def __get_end(self) -> Node:
        """get the endpoint node of the container instance"""
        current: self.Node = self.head
        while current.after is not None:
            current = current.after
        return current

    def __set_index(self):
        """set the index of all the nodes"""
        if not self.is_empty():
            current: self.Node = self.head
            new_index: int = 0
            while current.after is not None:
                current.index = new_index
                current = current.after
                new_index += 1

    @classmethod
    def __check_data_typing(cls, old_node: Node, new_data):
        """make sure that the data being added is the same type"""
        if not isinstance(old_node.data, type(new_data)):
            raise TypeError('data is not an instance of', type(old_node.data))

    def is_empty(self) -> bool:
        """checks if there is any data in the container instance"""
        return self.head is None

    def is_full(self) -> bool:
        """checks if the max amount of values are present in the container"""
        if self.max_size is not None:
            return self.size > self.max_size
        return False

    def enqueue_front(self, data):  # ? unused method
        """add data to the front of the container instance"""
        if self.is_empty():
            # ? overwrite the head Node
            self.head = self.Node(None, data, None)
        elif self.is_full():
            raise ValueError("The container is full")
        else:
            # prepend a new node to the front of the container instance
            old_head: self.Node = self.head
            self.__check_data_typing(old_head, data)
            new_head: self.Node = self.Node(None, data, old_head)
            old_head.before = new_head
            self.head = new_head
        # set the new indicies
        self.__set_index()
        # change the size of the container instance
        self.size += 1

    def dequeue_front(self) -> None:
        """remove data from the back of the container instance"""
        if self.is_empty():
            raise ValueError('cannot pop any values from an empty container')
        if self.is_full():
            raise ValueError("The container is full")
        old_head_node: self.Node = self.head
        return_data = old_head_node.data
        new_head_node: self.Node = None
        if old_head_node.after is not None:
            new_head_node = old_head_node.after
            new_head_node.before = None
        self.head = new_head_node
        del old_head_node
        self.size -= 1
        # set the new indicies
        self.__set_index()
        return return_data

    def peak_front(self) -> None:
        """see what is at the front of the container instance without popping the element"""
        if not self.is_empty():
            return self.head.data
        raise ValueError('the container is empty, there are no values to peak')

    def enqueue_back(self, data):
        """add data to the back of the container instance"""
        if self.is_empty():
            # ? overwrite the head Node
            self.head = self.Node(None, data, None)
        else:
            # append a new node to the end of the container instance
            old_endpoint: self.Node = self.__get_end()
            self.__check_data_typing(old_endpoint, data)
            # link Node pointers of old and new endpoint
            new_endpoint: self.Node = self.Node(old_endpoint, data, None)
            old_endpoint.after = new_endpoint
        # set the new indicies
        self.__set_index()
        # change the size of the container instance
        self.size += 1

    def dequeue_back(self) -> None:  # ? unused method
        """remove data from the front of the container instance"""
        if self.is_empty():
            raise ValueError('cannot pop any values from an empty container')
        return_value = self.head.data
        if self.size == 1:
            self.head = None
        else:
            old_endpoint: self.Node = self.__get_end()
            return_value = old_endpoint.data
            new_endpoint: self.Node = None
            if old_endpoint.before is not None:
                # ? destroy the link the the endpoint and the node before it (if its not NULL)
                new_endpoint = old_endpoint.before
                new_endpoint.after = None
                old_endpoint.before = None
                old_endpoint = None
                del old_endpoint
        self.size -= 1
        return return_value

    def peak_back(self) -> None:  # ? unused method
        """see what is at the front of the container instance without popping the element"""
        if not self.is_empty():
            return self.__get_end().data
        raise ValueError('the container is empty, there are no values to peak')


def promptint() -> int:
    """
    prompts the user for an postive integer and returns it
    Returns:
        int: postive integer from user input
    """
    while True:
        myinput = input('').strip()
        if not myinput.isdigit():
            print('you can only type in a positive integer')
        elif int(myinput) < 0:
            print('please type in a postive integer')
        else:
            return int(myinput)


class Base:  # pylint: disable=R0903
    """
    a superclass of the Ingredient class used to contain basic information about an ingredient
    """
    ingredient_name: str = ''
    amount_on_hand: int = 0
    amount_needed: int = 0
    amount_parent_made_per_craft: int = 0
    amount_resulted: int = 0
    queue_amount_resulted: dict = {}
    alias_ingredient: str = ''

    def __init__(self, ingredient_name: str = '',
                 amount_on_hand: int = 0,
                 amount_parent_made_per_craft: int = 1,
                 amount_needed: int = 1) -> None:
        """
        a superclass of the Ingredient class used to contain basic information about an ingredient
        Args:
            ingredient_name(str, optional): name of the item stored. Defaults to ''.
            amount_on_hand (int, optional): how much of the ingredient you have to craft the direct
            parent item above it. Defaults to 0.
            amount_parent_made_per_craft (int, optional): how much of the parent
            ingredient is made with
            this ingredient. Defaults to 1.
            amount_needed (int, optional): amount of ingredient needed to craft the
            parent ingredient
            once. Defaults to 1.
        """
        self.amount_on_hand = amount_on_hand
        self.amount_parent_made_per_craft = amount_parent_made_per_craft
        self.amount_needed = amount_needed
        self.queue_amount_resulted = {}
        self.ingredient_name = ingredient_name
        self.amount_resulted = 0
        self.alias_ingredient = ingredient_name.replace(' ', '_')


class Ingredient(Base):  # pylint: disable=R0913 #pylint: disable=R0902
    """
    primary class of the Ingredient, used to stored information about an ingredient as well as
    information to identify the ingredient and its parent ingredient
    """
    parent_ingredient = None
    children_ingredients: dict = {}
    generation: int = 0
    instances: int = 0
    instancekey: int = 0
    treekey: str = ''
    isfromcsvfile: bool = False
    population: int = 1

    def __init__(self, ingredient_name: str = '',  # pylint: disable=R0913
                 parent_ingredient=None,
                 amount_on_hand: int = 0,
                 amount_parent_made_per_craft: int = 1,
                 amount_needed: int = 1,
                 promptamountparentmade: bool = False,
                 promptamountsOn: bool = True,
                 isfromcsvfile: bool = False,
                 treekey: str = '') -> None:
        """
        primary class of the Ingredient, used to stored information about an ingredient as well as
        information to identify the ingredient and its parent_ingredient
        Args:
            ingredient (str, optional): name of the item stored. Defaults to ''.
            amount_on_hand (int, optional): how much of the ingredient you have to craft the direct
            parent ingredient above it. Defaults to 0.
            amount_parent_made_per_craft (int, optional): how much of the parent
            ingredient is made with this ingredient. Defaults to 1.
            amount_needed (int, optional): amount of ingredient needed to craft the parent
            ingredient once. Defaults to 1.
            promptamountparentmade (bool, optional): determines if the program should prompt user to
            type in a number for the amount of the parent ingredient made per craft.
            Defaults to False.
            isfromcsvfile (bool, optional): a boolean to track if the created Ingredient instance is
            from the CSV file. Defaults to False.
            treekey (str, optional): a string of about 10 to 20 alphanumeric characters to help make
            each ingredient tree unique when written to a CSV file. Defaults to ''.
        """
        super().__init__(ingredient_name,
                         amount_on_hand,
                         amount_parent_made_per_craft,
                         amount_needed)
        self.treekey = treekey
        self.isfromcsvfile = isfromcsvfile
        self.instancekey = Ingredient.instances
        self.children_ingredients = {}
        self.parent_ingredient = parent_ingredient
        if self.parent_ingredient is not None:
            self.generation = self.parent_ingredient.generation + 1
            self.parent_ingredient.children_ingredients.update(
                {self.instancekey: self})
            self.treekey = self.parent_ingredient.treekey
        else:
            self.generation = 0
            if isfromcsvfile:
                self.treekey = treekey
            else:
                self.treekey = self.gen_treekey()
        if promptamountsOn and __name__ == '__main__':
            self.__inputnumerics(promptamountparentmade)
        self.updatepopulation()
        Ingredient.instances += 1

    def __inputnumerics(self, promptamountparentmade: bool):
        """
        prompt input of the numeric data for the instance from the user
        """
        # $ only in MODE A - prompt amount_on_hand
        while MODE == ProgramState.MODE_A:
            print('How much', self.ingredient_name, 'do you have on hand: ')
            self.amount_on_hand = promptint()
            if self.amount_on_hand < 0:
                print('That number is not valid')
            else:
                break
        if self.parent_ingredient is not None:
            # $ only if older sibiling has not been prompted, prompt amountmadepercraft
            while promptamountparentmade:  # ? should this be prompted depending on if it was cloned
                print('How much', self.parent_ingredient.ingredient_name,
                      'do you create each time you craft it: ')
                self.amount_parent_made_per_craft = promptint()
                if self.amount_parent_made_per_craft < 1:
                    print('That number is not valid')
                else:
                    promptamountparentmade = False
                    break
            # $ prompt amount_needed
            while True:
                print('How much', self.ingredient_name, 'do you need to craft',
                      self.parent_ingredient.ingredient_name, '1 time: ')
                self.amount_needed = promptint()
                if self.amount_needed < 1:
                    print('That number is not valid')
                else:
                    break

    @classmethod
    def gen_treekey(cls, maxlength: int = random.randint(10, 20)) -> str:
        """
        generate a unique tree key of random alphumeric characters
        """
        cls.treekey = ''
        for _ in range(0, maxlength):
            cls.treekey += random.choice(
                '0123456789abcdefghijklmnopqrstuvwxyz')
        return cls.treekey

    def recursivearithmetic(self) -> int:
        """
        tentative docstring description
        """
        # check and set minimum resulted if queue is not empty
        tentativeinteger: int = sys.maxsize
        if len(self.queue_amount_resulted) == 0:
            tentativeinteger = 0
        else:
            for myinteger in self.queue_amount_resulted.items():
                if myinteger[1] < tentativeinteger:
                    tentativeinteger = myinteger[1]
        red = (self.amount_parent_made_per_craft / self.amount_needed)
        blue = (red*self.amount_on_hand) + (red*tentativeinteger)
        blue = round(math.floor(blue))
        self.amount_resulted = blue
        # recursively call the method
        if self.parent_ingredient is not None:
            self.parent_ingredient.queue_amount_resulted.update(
                {self.ingredient_name: self.amount_resulted})
            self.parent_ingredient.recursivearithmetic()
        return self.amount_resulted

    def reversearithmetic(self, desiredamount: int = 0) -> int:
        """
        tentative docstring description
        """
        self.amount_resulted = desiredamount
        red: float = ((self.amount_parent_made_per_craft/self.amount_needed)
                      ** -1)*self.amount_resulted
        green: float = round(math.ceil(red))
        self.amount_on_hand = int(max(red, green))
        traceback: bool = green > red
        if traceback:  # traverse upward and increase the amount on hand by 1
            temp: Ingredient = self
            while temp.parent_ingredient is not None:
                temp = temp.parent_ingredient
                temp.amount_on_hand += 1
        # continue method recursively
        if len(self.children_ingredients) > 0:
            for childnode in self.children_ingredients.items():
                if not isinstance(childnode[1], Ingredient):
                    raise TypeError('child is not an instance of', Ingredient)
                childnode[1].reversearithmetic(self.amount_on_hand)
        return self.amount_on_hand

    def modifytreekey(self, newtreekey: str):
        """
        change the tree key of the ingredient and all of its children ingredients
        """
        self.treekey = newtreekey
        for subnode in self.children_ingredients.items():
            subnode[1].modifytreekey(newtreekey)

    def pandasrow(self) -> dict:
        """
        create a row of data of the Ingredient for writing to the csv file
        Returns:
            dict: a dict of information about the Ingredient
        """
        pandas_row: dict = {}
        pandas_row.update({'Tree_Key': self.treekey})
        pandas_row.update({'Ingredient': self.ingredient_name})
        pandas_row.update({'Ingredient_Alias': self.alias_ingredient})
        if self.parent_ingredient is not None:
            pandas_row.update(
                {'Parent_of_Ingredient': self.parent_ingredient.ingredient_name})
        else:
            pandas_row.update({'Parent_of_Ingredient': 'None'})
        pandas_row.update({'Amount_on_Hand': str(self.amount_on_hand)})
        pandas_row.update(
            {'Amount_Made_Per_Craft': str(self.amount_parent_made_per_craft)})
        pandas_row.update(
            {'Amount_Needed_Per_Craft': str(self.amount_needed)})
        pandas_row.update({'Generation': str(self.generation)})
        return pandas_row

    def pandastree_row(self, rows: Deque) -> Deque:
        """
        return a list of all the pandas rows in the tree
        Args:
            rows (list): a list of pandas rows (dicts of data)
        Returns:
            list: a list of dicts containing the data for each ingredient to be written
            onto a csv file
        """
        enqueued_data = self.pandasrow()
        rows.enqueue_back(enqueued_data)
        for child in self.children_ingredients.items():
            child[1].pandastree_row(rows)
        return rows

    def updatepopulation(self, population: int = 0):
        """
        sets and updates the population attribute of the Ingredient accordingly
        """
        self.population = population
        for subnode in self.children_ingredients.items():
            subnode[1].updatepopulation(population)

    def findendpoints(self, endpoints: dict) -> dict:
        """
        returns a dictionary of nodes with no children ingredients
        Args:
            endpoints (dict): _description_
        Returns:
            _type_: _description_
        """
        for subnode in self.children_ingredients.items():
            if len(subnode[1].children_ingredients) == 0:
                endpoints.update({subnode[1].instancekey: subnode[1]})
            else:
                subnode[1].findendpoints(endpoints)
        return endpoints

    def reformat_output(self):  # pylint:disable=R0912
        """
        condenses the output of the tree into a more readable format with percentages
        """
        # ! this method can only run when there is are more than one nodes in the ingredient tree,
        # ! otherwise it will crash
        # set the new dictionary to be empty
        temp = self
        if not isinstance(temp, Ingredient):
            raise TypeError('temp is not an instance of', Ingredient)
        while temp.parent_ingredient is not None:
            temp = temp.parent_ingredient
        compressedendpoints: dict = {}
        # set the new dictionary to have unique ingredients as keys
        # and a list of tuples of the parent_ingredient object of said endpoint instance and the
        # amount on hand as values
        for ingredient_node in temp.findendpoints({}).items():
            if ingredient_node[1].ingredient_name not in compressedendpoints:
                compressedendpoints.update(
                    {ingredient_node[1].ingredient_name:
                        [(ingredient_node[1].parent_ingredient.ingredient_name,
                          ingredient_node[1].amount_on_hand)]})
            else:
                compressedendpoints[ingredient_node[1].ingredient_name].append(
                    (ingredient_node[1].parent_ingredient.ingredient_name,
                     ingredient_node[1].amount_on_hand))
        output_dictionary: dict = {}
        for item_a in compressedendpoints.items():
            orangeinteger: int = 0  # sum of the amount on hand all tuple items
            for orangenumber in item_a[1]:
                orangeinteger += orangenumber[1]
            for orangetuple in item_a[1]:
                if item_a[0] not in output_dictionary:
                    output_dictionary.update({item_a[0]: [str(round(
                        (orangetuple[1]/orangeinteger)*100, 2)) +
                        '% ('+str(orangetuple[1])+'x) used in ' +
                        orangetuple[0]]})
                else:  # if item is in the dict, append the string to list
                    output_dictionary[item_a[0]].append(
                        str(round((orangetuple[1]/orangeinteger)*100, 2)) +
                        '% ('+str(orangetuple[1])+'x) used in ' +
                        orangetuple[0])
        # output the dictionary keys and values
        for item_a in output_dictionary.items():
            print(item_a[0], end=' (')
            for index, string in enumerate(item_a[1]):
                if index == len(item_a[1])-1:
                    print(string, end='')
                else:
                    print(string, end=', ')
            print(')')


def nodecount(ingredient: Ingredient) -> int:
    """
    counts how many nodes are in the connected ingredient tree
    Returns:
        int: the number of nodes in the tree (based on the size of list of nodes)
    """
    size_of_deque: int = head(ingredient).pandastree_row(Deque()).size
    #!len(head(ingredient).pandastree_row(Deque()))
    return size_of_deque


def makealiasunique(ingredient: Ingredient):
    """
    makes all the ingredient aliases in the ingredient tree unique
    Args:
        ingredient (Ingredient): current ingredient object
    """
    # make all nodes in the tree have unique ingredient aliases
    # get a list of all the nodes in the ingredient tree with the same ingredient alias
    # as the passed ingredient instance
    nodesaliases: Deque = allaliases(
        ingredient, ingredient.alias_ingredient, Deque())
    # if the list is greater than 1, then parse through the list to make each alias unique
    if nodesaliases.size > 1:
        # make uniue by appending the index to the alias
        #!    for redindex, reditem in enumerate(nodesaliases):
        #!        for blueindex, blueitem in enumerate(nodesaliases):
        #!            if redindex != blueindex and reditem.alias_ingredient == blueitem.alias_ingredient:
        #!                blueitem.alias_ingredient += str(blueindex)
        nodesaliases.dequeue_front()
        node_ingredient_duplicate_num: int = 2
        while not nodesaliases.is_empty():
            if not isinstance(nodesaliases.peak_front(), Ingredient):
                raise TypeError(
                    'peaked value from the deque is not an instance of', Ingredient)
            ingredient_object: Ingredient = nodesaliases.dequeue_front()
            ingredient_object.alias_ingredient += str(
                node_ingredient_duplicate_num)
            node_ingredient_duplicate_num += 1
    # recrusively call the function on each child ingredient
    for subnode in ingredient.children_ingredients.items():
        makealiasunique(subnode[1])


def allaliases(ingredient: Ingredient, alias: str, aliases: Deque) -> Deque:
    """
    returns a list of all the nodes with the same alias
    Args:
        ingredient (Ingredient): ingredient to check if it has the same ingredient alias value
        alias (str): nickname of Ingredient instance
        aliases (list): list of nodes with the same alias to search for
    Returns:
        list: a list of Nodes containining the same ingredient alias
    """
    if ingredient.alias_ingredient == alias:
        aliases.enqueue_back(ingredient)
    # recrusively search for nodes that have the same ingreident alias as the passed alias
    for subnode in ingredient.children_ingredients.items():
        allaliases(subnode[1], alias, aliases)
    return aliases


def writetreetocsv(ingredient: Ingredient):
    """
    writes an ingredient tree onto a csv file
    Args:
        ingredient (Ingredient): the head ingredient of the ingredient tree
    """
    # check if the csv file exists
    # if the file is not in the directory, create it
    if not os.path.exists(FILENAME):
        # create the file
        pandas.DataFrame(columns=FIELDNAMES).to_csv(
            FILENAME, index=False)
        # open file again to append to it
        writetreetocsv(ingredient)
    else:
        # then write to the file but calling the method again recursively
        # ? make sure to check this, used to be an empty list prior to change
        #! for row in ingredient.pandastree_row(Deque()):
        #!    pandas.DataFrame(row, index=[0]).to_csv(
        #!        FILENAME, mode='a', header=False, index=False)
        csvrows_deque: Deque = ingredient.pandastree_row(Deque())
        while not csvrows_deque.is_empty():
            pandas.DataFrame(csvrows_deque.dequeue_front(), index=[0]).to_csv(
                FILENAME, mode='a', header=False, index=False)


def promptheadname() -> str:
    """
    prompts the user for the head ingredient name
    Returns:
        str: the name of the head ingredient
    """
    while True:
        myinput: str = input('What is the name of the item you are trying to make: ').strip()  # noqa: E501 #pylint: disable=line-too-long
        if len(myinput) == 0:
            print('Your input cannot be empty!')
        else:
            return myinput


def head(ingredient: Ingredient) -> Ingredient:
    """
    traverse to the parent most Ingredient
    Args:
        ingredient (Ingredient): starting Ingredient
    Returns:
        Ingredient: parent most Ingredient of the starting Ingredient
    """
    while ingredient.parent_ingredient is not None:
        ingredient = ingredient.parent_ingredient
    return ingredient


def trail(ingredient: Ingredient):
    """
    print the ingredient trail leading up to the parent most Ingredient
    Args:
        ingredient (Ingredient): starting Ingredient
    """
    print('TRAIL: ', end='')
    while True:
        if ingredient.parent_ingredient is not None:
            print(ingredient.ingredient_name, '-> ', end='')
            ingredient = ingredient.parent_ingredient
        else:
            print(ingredient.ingredient_name)
            break


def outputingredients(ingredient: Ingredient):
    """
    populate submethod, print the subingredients of the parameter Ingredient
    Args:
        ingredient (Ingredient): parent ingredient, the ingredient to print the subingredients of
    """
    subingredients: list = []
    for subnode in ingredient.children_ingredients.items():
        subingredients.append(subnode[1].ingredient_name)
    print('+ These ingredients are already in the tree:\n')
    # output the ingredients
    for index, ingredient in enumerate(subingredients):
        print(f'{index+1}. {ingredient}')
    print('')


def parsecsv() -> dict:
    """
    parses the csv file to look for head nodes, returns a dictionary of them
    Returns:
        dict: dictionary of head ingredient instances from the csv file, key is the treekey
        and the value is the head ingredient instance
        will return a dict of {-1:None} if unable to find any
    """
    headnodes: dict = {}
    # if there are no head nodes,
    # or the file does not exist return {-1: None}
    if not os.path.exists(FILENAME):
        return {-1: None}
    # parse csv for head nodes
    for purple in pandas.read_csv(FILENAME).to_dict('index').items():
        # convert the values of the dictionary to a list to see if it holds valid values
        green: list = list(purple[1].values())
        if green[3] == 'None' and green[5] == 1 and green[6] == 1 and green[7] == 0:
            headnodes.update({green[0]: Ingredient(ingredient_name=green[1],
                                            parent_ingredient=None,
                                            promptamountparentmade=False,  # noqa: E501 #pylint: disable=line-too-long
                                            treekey=green[0],
                                            isfromcsvfile=True,
                                            promptamountsOn=False)})
    if len(headnodes) == 0:
        return {-1: None}
    return headnodes


def createtree(ingredient: Ingredient, pandasrow: Deque) -> bool:
    """
    figure out where to emplace the Ingredient in the tree
    Args:
        ingredient (Ingredient): parent of Ingredient to be emplaced
        pandasrow (list): row of data from the CSV file
    Raises:
        TypeError: the row of data contains an invalid amount of values
    Returns:
        bool: was the ingredient actually emplaced
    """
    deque_peak_value: list = pandasrow.peak_front()
    if len(deque_peak_value) != len(FIELDNAMES):
        raise TypeError('The row of data is not the correct length')
    # remove any underscores from the ingredient
    deque_peak_value[1] = deque_peak_value[1].replace('_', ' ')
    # remove any underscores from the parent of the ingredient
    deque_peak_value[3] = deque_peak_value[3].replace('_', ' ')
    foundemplacelocation: bool = ingredient.treekey == deque_peak_value[0] and deque_peak_value[
        3] != 'None' and deque_peak_value[3] == ingredient.ingredient_name and deque_peak_value[7] > 0 and ingredient is not None and deque_peak_value[7] == ingredient.generation + 1  # noqa: E501 #pylint: disable=line-too-long
    if foundemplacelocation:
        data_row_dequeued: list = pandasrow.dequeue_front()
        Ingredient(data_row_dequeued[1],
                   parent_ingredient=ingredient,
                   amount_needed=data_row_dequeued[6],
                   amount_parent_made_per_craft=data_row_dequeued[5],
                   amount_on_hand=data_row_dequeued[4],
                   treekey=data_row_dequeued[0],
                   # isfromcsvfile=True,
                   promptamountsOn=False)
        red: str = '\x1B[31m' + ingredient.ingredient_name + \
            '\x1B[0m'  # parent ingredient namedeque_peak_value
        blue: str = '\x1B[36m' + data_row_dequeued[1] + \
            '\x1B[0m'  # ingredient name
        print('emplaced ingredient', red + ' | ' + blue)
        return True
    for subnode in ingredient.children_ingredients.items():
        createtree(subnode[1], pandasrow)
    return False


def createtreefromcsv(parent_ingredient: Ingredient) -> Ingredient:
    """
    figures out where to create and link a new ingredient object from the csv file
    Args:
        parent_ingredient (Ingredient): potential parent ingredient object to link new
        ingredient object to pandasrow (list): data from csv file, creates ingredient object from it
    Returns:
        Ingredient: parent most ingredient object of the tree
    """
    # check if the row has the correct amount of elements
    # the ingredient object must match the following requirements to link:
    # parent ingredient must be the same as the parent ingredient
    # treekey must be the same & generation > 0
    #! sublist: list = []
    sublist: Deque = Deque()
    for purple in pandas.read_csv(FILENAME).to_dict('index').items():
        # convert the values of the dictionary to a list
        green: list = list(purple[1].values())
        # if the tree key of the row matches the head ingredient object's tree key
        if green[0] == parent_ingredient.treekey and green[3] != 'None':
            # the sublist contains ingredient object only from the tree
            #! sublist.append(green)
            sublist.enqueue_back(green)
    # figure out where to emplace the ingredient object
    # $ correctly finds all nodes with the same treekey from the csv file
    #! for row in sublist:
        #! createtree(parent_ingredient, row)
    while not sublist.is_empty():
        createtree(parent_ingredient, sublist)
        # print('row', index, 'of', len(sublist), 'rows')
    return head(parent_ingredient)


def search(ingredient: Ingredient, ingredient_name: str, results: list) -> list:
    """
    recursively search through the tree to find nodes with the same
    ingredient
    Args:
        ingredient (Ingredient): parent ingredient object, parse through its children ingredients recursively to
        update the search results
        ingredient (str): the name of the item you are searching for
        results (list): nodes that have the same ingredient as the parameter
    Returns:
        list: a list of nodes that have the same ingredient as the parameter
    """
    # if ingredient object is a subnode and the ingredient matches, update the list
    if ingredient.parent_ingredient is not None and ingredient.ingredient_name == ingredient_name:
        results.append(ingredient)
    # recrusively keep searching for nodes
    for subnode in ingredient.children_ingredients.items():
        search(subnode[1], ingredient_name, results)
    return results


def shouldclonechildren(ingredient: str, subnodes: dict) -> bool:
    """
    check to see if the ingredient is within the subnodes of its siblings nodes of its emplace
    location
    Args:
        ingredient (str): name of item to check if it is in the subnodes
        subnodes (dict): a dictionary of subnodes of the parent ingredient
        object (emplace parent location)
    Raises:
        TypeError: dictionary does not contain int, ingredient object pairs
        TypeError: the parent_ingredient object of the subnodes are not the same
    Returns:
        bool: whether or not the ingredient is in the subnodes, used to help determine if the
        subnodes should be cloned
    """
    if len(subnodes) == 0:
        return True
    # convert subnodes dict to a list of nodes
    subnodeslist: list = []
    for subnode in subnodes.items():
        # dict must be have a key integer and a Ingredient instance as the value
        if not isinstance(subnode[1], Ingredient) and not isinstance(subnode[0], int):
            raise TypeError('subnodes is not a dictionary',
                            Ingredient, 'subnodes')
        # check if any ingredient object instance in the convert list does
        # not have a the same parent_ingredient
        # raise an error if the parent_ingredient object is not the same in all nodes
        subnodeslist.append(subnode[1])
        for redindex, rednode in enumerate(subnodeslist):
            for blueindex, bluenode in enumerate(subnodeslist):
                if redindex != blueindex and rednode.parent_ingredient is not bluenode.parent_ingredient:
                    raise TypeError('subnodes is not a dictionary',
                                    Ingredient, 'subnodes with the same parent_ingredient object')
    # create a list of ingredient names that are within all the nodes in the dict
    subingredientnames: list = []
    for subnode in subnodeslist:
        for childnode in subnode.children_ingredients.items():
            subingredientnames.append(childnode[1].ingredient_name)
    # check if the ingredient is in the list of subingredient names
    if ingredient in subingredientnames:
        return False
    return True


def clone(ingredient: Ingredient, clonechildren: bool = True) -> Ingredient:
    """
    creates a returnable clone of the ingredient passed into the method
    Args:
        ingredient (Ingredient): current ingredient instance to copy and clone
        clonechildren (bool, optional): should the have its subnodes cloned aswell.
        Defaults to True.
    Returns:
        Ingredient: a clone of a ingredient
    """
    # (industrial battery GEN==1, input protocite)
    # if the parent ingredient is in the same generation as the clone,
    # do not clone the children ingredients, set the parent as its grandparent ingredient

    # create a copy of the parameter ingredient
    if not clonechildren:
        if ingredient.parent_ingredient is not None and ingredient.parent_ingredient.parent_ingredient is not None and isinstance(ingredient.parent_ingredient.parent_ingredient, Ingredient):  # pylint:disable = line-too-long
            bluenode: Ingredient = Ingredient(ingredient_name=ingredient.ingredient_name,
                                              parent_ingredient=ingredient.parent_ingredient.parent_ingredient,
                                              amount_on_hand=ingredient.amount_on_hand,
                                              amount_needed=ingredient.amount_needed,
                                              amount_parent_made_per_craft=ingredient.amount_parent_made_per_craft,
                                              isfromcsvfile=ingredient.isfromcsvfile,
                                              promptamountsOn=False)
            return bluenode
        # fallback incase grandparent is not valid
        # $ go back and examine this return branch more
        return clone(ingredient, True)
    rednode: Ingredient = Ingredient(ingredient_name=ingredient.ingredient_name,
                                     parent_ingredient=ingredient.parent_ingredient,
                                     amount_on_hand=ingredient.amount_on_hand,
                                     amount_needed=ingredient.amount_needed,
                                     amount_parent_made_per_craft=ingredient.amount_parent_made_per_craft,
                                     isfromcsvfile=ingredient.isfromcsvfile,
                                     promptamountsOn=False)
    # create a copy of all the children ingredients of the parameter ingredient object
    for subnode in ingredient.children_ingredients.items():
        Ingredient(ingredient_name=subnode[1].ingredient_name,
                parent_ingredient=subnode[1],
                amount_on_hand=subnode[1].amount_on_hand,
                amount_needed=subnode[1].amount_needed,
                amount_parent_made_per_craft=subnode[1].amount_parent_made_per_craft,  # noqa: E501 #pylint: disable=line-too-long
                promptamountparentmade=False,
                isfromcsvfile=subnode[1].isfromcsvfile,
                promptamountsOn=False)
    return rednode


def subpopulate(ingredient: Ingredient, ingredient_name: str) -> Ingredient:
    """
    create a subnode and link it to the parent ingredient
    Args:
        ingredient (Ingredient): parent Ingredient to link back to
    Returns:
        Ingredient: new subnode to link back to the parent Ingredient
    """
    # create a list of subnodes that have the same ingredient as the parameter
    parseresults: list = search(head(ingredient), ingredient_name, [])
    # if the list is empty return a defaultly created new ingredient Ingredient
    for subnode in parseresults:
        if not isinstance(subnode, Ingredient):
            raise TypeError(
                'item in the list is not an instance of', Ingredient)
    if len(parseresults) == 0:
        return Ingredient(ingredient_name, ingredient)
    # else, prompt the user to create a linkable clone of the new ingredient
    print('+ parent ingredient (item that,', ingredient_name, 'creates somewhere else in your ingredient tree)\n'
          '++ amount of', ingredient_name,
          'on hand (needed to make 1', head(ingredient).ingredient_name, end=')\n')
    print('+++ amount of the parent ingredient made per craft')
    print('++++ amount Needed to craft parent ingredient item once\n')
    if MODE == ProgramState.MODE_B:
        head(ingredient).reversearithmetic(1)
    for index, subnode in enumerate(parseresults):
        # come back to this and see if do the math on the tree
        # will help differiate the values (industral battery)

        # output the choices of subnodes:
        # parent ingredient, amount_needed, amountmadepereachcraft
        print(index+1, end=str('. + ' + subnode.parent_ingredient.ingredient_name
                               + ' | ++ ' + str(subnode.amount_on_hand)
                               + ' | +++ ' + str(subnode.amount_needed)
                               + ' | ++++ ' + str(subnode.amount_parent_made_per_craft)+'\n'))
    # todo make sure program doesn't crash when user's input is blank
    print('Choose which verison of', ingredient_name, 'to clone:')
    userchoice: int = promptint() - 1
    # if the user chooses to create a new ingredient object, return a clone subnode
    if userchoice < 0 or userchoice > len(parseresults)-1:
        # if the user did not input a valid index
        # if not return the defaultly created new ingredient object
        return Ingredient(ingredient_name, ingredient)
    # check if the ingredient is in any of the subnodes of its sibilings
    clonenode: Ingredient = clone(
        parseresults[userchoice],  # ingredient that will be cloned
        shouldclonechildren(ingredient_name,
                            ingredient.children_ingredients))  # bool to determine to clone subnodes
    return clonenode


def populate(ingredient: Ingredient) -> Ingredient:  # pylint: disable=R0912
    """
    create a tree of Nodes
    Args:
        ingredient (Ingredient): parent the subnodes will be linked to
    Returns:
        Ingredient: the head of the ingredient tree
    """
    # update population attribute of Ingredient
    ingredient.updatepopulation(nodecount(ingredient))
    # output the ingredient trail if there is a parent Ingredient
    if ingredient.parent_ingredient is not None:
        trail(ingredient)
    # prompt the user to ingredient tree
    user_inputs: Deque = Deque()  # list of tuples (string, bool)
    ingredient_blacklist: list = []
    # append subnode ingredients to the list if there are any
    for subnode in ingredient.children_ingredients.items():
        #! user_inputs.enqueue_back((subnode[1].ingredient_name, True))
        # ? ingredient_name, already created boolean (which is true)
        ingredient_blacklist.append(subnode[1].ingredient_name)
    # prompt the user for ingredients
    print('What ingredients do you have need to create',
          ingredient.ingredient_name, end=':\n')
    # if there are subnodes, prompt the user to select from the list
    if len(ingredient.children_ingredients) > 0:
        outputingredients(ingredient)
    while True:
        # prompt the user for an ingredient
        myinput: str = input('').strip()
        # check to see if the user input is the same as the parent or head Ingredient
        if myinput in [head(ingredient).ingredient_name, ingredient.ingredient_name]:
            print('Invalid input, we are trying to make that item!')
        # if the length of the user input is 0, break the loop
        elif myinput in ingredient_blacklist:
            print('Invalid input, duplicate inputs!')
        # if the input is empty, break out of the loop
        elif len(myinput) == 0:
            break
        # append to the user inputs list if all the checks pass
        else:
            # if the condition is met, append the input to the list
            #! user_inputs.enqueue_back((myinput, False))
            user_inputs.enqueue_back(myinput)
            # ? ingredient_name, already created boolean (which is true)
            ingredient_blacklist.append(myinput)
    # create subnodes for each ingredient using the subpopulate method
    while not user_inputs.is_empty():
        # if ingredient[1] is False, the ingredient is not already in the tree (from csv)
        #! deque_peak_front: tuple = user_inputs.peak_front()
        #! if not deque_peak_front[1]:
        # searchresults: list = search(head(ingredient), ingredient[0], [])
        subpopulate(ingredient, user_inputs.dequeue_front())

    # update population attribute of Ingredient
    ingredient.updatepopulation(nodecount(ingredient))
    # recrusively continue to populate the tree
    # ! sometimes runtime error occurs, cloning a child of the same parent?
    for subnode in ingredient.children_ingredients.items():
        populate(subnode[1])
    # if the program Mode is A and the length of the children ingredients are 0
    if MODE == ProgramState.MODE_A and len(ingredient.children_ingredients) == 0:
        # call the arithmetic method
        ingredient.recursivearithmetic()
    # return the head of the ingredient tree
    return head(ingredient)


def superpopulate() -> Ingredient:
    """
    creates an ingredient tree and returns its head ingredient
    Returns:
        Ingredient: head ingredient of the populated ingredient tree
    """
    # check to see if there is a csv file in the current directory
    if not os.path.exists(FILENAME):
        # if the file exists, parse it for head nodes
        ingredient_tree: Ingredient = head(
            populate(Ingredient(promptheadname())))
        ingredient_tree.modifytreekey(ingredient_tree.gen_treekey())
        return ingredient_tree
    # parse the csv file for head nodes
    foundheadnodes: dict = parsecsv()
    # if there are no head nodes {-1:None}
    if foundheadnodes == {-1: None}:
        # return new ingredient tree
        ingredient_tree: Ingredient = head(
            populate(Ingredient(promptheadname())))
        ingredient_tree.modifytreekey(ingredient_tree.gen_treekey())
        return ingredient_tree
    userchoices: list = []
    # convert the dict into a list of ingredient instances
    for ingredient in foundheadnodes.items():
        userchoices.append(ingredient[1])
    # sort the list of nodes by the amount of children ingredients
    for blue in range(0, len(userchoices)-1):
        for red in range(0, len(userchoices)-1):
            if not isinstance(userchoices[red], Ingredient):
                raise TypeError(
                    'item in the list is not an instance of', Ingredient)
            if head(userchoices[blue]).instancekey > head(userchoices[red]).instancekey:
                # flake8: noqa
                userchoices[blue], userchoices[red] = userchoices[red], userchoices[blue]
                # swap red and blue
    # output the choices
    print('Do you want to choose from one of the following trees as a preset?')
    for index, ingredient in enumerate(userchoices, start=1):
        print(index, end=str('. ' + ingredient.ingredient_name)+'\n')
    # prompt the user to make select a head ingredient to modify
    print('Please choose a head ingredient node to modify, select a number out of range to create a new tree')
    userchoice: int = promptint()-1
    # if the user chosesn an index out or range, return a new tree
    if userchoice < 0 or userchoice > len(userchoices)-1:
        ingredient_tree: Ingredient = head(
            populate(Ingredient(promptheadname())))
        ingredient_tree.modifytreekey(ingredient_tree.gen_treekey())
        return ingredient_tree
    # return the head ingredient node of the chosen tree
    # create ingredient tree out of the csv file
    ingredient_tree: Ingredient = head(
        populate(createtreefromcsv(userchoices[userchoice])))
    ingredient_tree.modifytreekey(ingredient_tree.gen_treekey())
    return ingredient_tree


def prompt_print():
    """print the operations the user has the ability to perform with the script
    """
    print('Which mode do you want to use:')
    print('Mode A - You are trying to figure out how much of your desired'
          ' item you can make with the current supply of materials'
          ' (Type in A)')
    print('Mode B - You are trying to figure out how much base materials'
          ' you need to create a certain amount of your desired item, ('
          'Type in B)')
    print("Type in 'H' if you need a reminder of the prompt\n")


if __name__ == '__main__':
    MODE: ProgramState = ProgramState.MODE_A
    # prompt program mode
    print('Welcome to Process Map (Python) v2.0!\n')
    # program runtime loop
    while True:
        prompt_print()
        # prompt user which mode they want to run the program in
        while True:
            userinput = input('').strip().upper()
            if userinput not in ('A', 'B', 'H'):
                print("That input is not valid, please type in 'A' or 'B'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      'character')
            elif userinput == 'B':
                MODE = ProgramState.MODE_B
                break
            elif userinput == 'H':
                # print prompt again
                prompt_print()
            else:
                MODE = ProgramState.MODE_A
                break
        # populate the ingredient tree
        ingredienttree: Ingredient = superpopulate()
        # if the programde mode is B
        if MODE == ProgramState.MODE_B:
            # prompt the user for how much an item they want to make
            print('How much of the item do you want to make?')
            ingredienttree.reversearithmetic(promptint())
        # $ this is where results of the arithmetic methods would be printed
        # ? if MODE B and population > 1
        if ingredienttree.population >= 2 and MODE == ProgramState.MODE_B:
            ingredienttree.reformat_output()
            print('\n')
        # ? if MODE A and population > 1
        elif ingredienttree.population >= 2 and MODE == ProgramState.MODE_A:
            print('You can make', ingredienttree.amount_resulted, 'of',
                  ingredienttree.ingredient_name, 'with the materials you have')
            # ? output the endpoint ingredient names and amounts resulted
            for item in ingredienttree.findendpoints({}).items():
                print('You would use',
                      item[1].amount_resulted, 'of', item[1].ingredient_name)
        # ? population == 1
        else:
            print('You would need', ingredienttree.amount_resulted, 'to create',
                  ingredienttree.amount_resulted, 'of', ingredienttree.ingredient_name)
        # prompt the user if they want to output the ingredient tree onto A csv file
        print('Do you want to save your tree to create',
              ingredienttree.ingredient_name, 'to a csv file? (Y/N)')
        while True:
            userinput = input('').strip().upper()
            if userinput not in ('Y', 'N'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      ' character')
            elif userinput == 'Y':
                # change the tree key
                ingredienttree.modifytreekey(
                    ingredienttree.gen_treekey())
                # make sure each ingredient alias is unique
                makealiasunique(ingredienttree)
                # write onto file
                writetreetocsv(ingredienttree)
                break
            else:
                break
        # prompt the user to see if they want to run the program again
        while True:
            userinput = input('\nDo you want to run the program again with'
                              ' another item tree? (Y/N) ').strip().upper()
            if userinput not in ('Y', 'N'):
                print("That input is not valid, please type in 'Y' or 'N'")
            elif len(userinput) > 1:
                print('Your input is too long, please only type in one'
                      ' character')
            else:
                break
        if userinput == 'N':
            break
    # close program in 10 seconds
    print('the program will close in 10 seconds')
    NANI: int = 10
    while NANI > 0:
        time.sleep(1)
        NANI -= 1
    print('terminating program')
# end main
