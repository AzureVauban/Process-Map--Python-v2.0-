"""
Unit Testing for Issue5:
Create a Tree Key alpha numeric string generator to make sure each tree in the .csv file is unique.
Fixes #5
"""
import csv
import os
import unittest

from main import Node  # pylint: disable=import-error

filename: str = 'ingredient_trees.csv'


class keygeneration(unittest.TestCase): #pylint: disable=invalid-name
    """
    Unit Testing for Issue5
    """

    def testkey(self):  # status : passed
        """test key"""
        red: Node = Node()
        testkey: str = red.generate_treekey()  # pylint: disable=no-member
        self.assertTrue(isinstance(testkey, str))

    def testkeyuniqueness(self):  # status : passed
        """test the uniqueness of the key
        """
        allkeysisunique: bool = True
        listofkeys: list = []
        # create some keys and append it to the list
        for red in range(10):
            listofkeys.append(Node.generate_treekey()
                              )  # pylint: disable=no-member
        # check for uniqueness within the list
        for index_red, red in enumerate(listofkeys):
            for index_blue, blue in enumerate(listofkeys):
                if red == blue and index_red != index_blue:
                    allkeysisunique = False

        self.assertTrue(allkeysisunique, 'The keys are not unique')

field_names = [
            'Tree_Key',  # 74nry8keki
            'Ingredient',  # Coal
            'Parent_of_Ingredient',  # Carbon
            'Amount_on_Hand',  # 0
            'Amount_Made_Per_Craft',  # 1
            'Amount_Needed_Per_Craft',  # 10
            'Generation'  # 1
        ]
class TestCSV(unittest.TestCase):
    """
    create a mock csv file and test the write_to_csv
    """
    # mock ingredient tree for carbon csv file
    carbon: Node = Node('Carbon', None, 0, 1, 1)
    coal: Node = Node('Coal', carbon, 0, 1, 10)
    pixels: Node = Node('Pixels', coal, 0, 1, 20)
    fileexistsalready : bool = os.path.isfile(filename)
    def testcsvlinedict(self):
        """test the csv line dict creation method"""
        mi_go: list = self.carbon.create_csv_writerows([])
#!      make sure to manually reverse the list before utilizing it
        self.assertTrue(isinstance(mi_go, list))

    def test_existance(self):
        """test if the file exists in the current directory
        """
        ispresentindirectory: bool = os.path.isfile(filename)
        # test if the file exists in the current folder of the directory

        rows: list = [  # pylint: disable=unused-variable
            {
            'Tree Key': '# 74nry8keki',
            'Ingredient': 'Coal',
            'Parent_of_Ingredient': 'Carbon',
            'Amount_on_Hand': '0',
            'Amount_Made_Per_Craft': '1',
            'Amount_Needed_Per_Craft': '10',
            'Generation': '1'
            }
        ]
        if ispresentindirectory:  # file already exists, write data to it
            with open(filename, mode='w', encoding='UTF-8',newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
#!                kassogtha :list = self.carbon.create_csv_writerows([])
#!              writer.writerow(self.carbon.create_csv_writerows([]))
                kassogtha: list = self.carbon.create_csv_writerows([])
            #!    for golonac in kassogtha:
            #!        writer.writerow(golonac)
                writer.writerows(kassogtha)
                csvfile.close()
        else:  # file does not exist, create it and write data to it
            #!          open file in write mode with UTF8 encoding
            with open(filename, mode='w', encoding='UTF-8',newline='') as nyarlathotep:
                writer = csv.DictWriter(nyarlathotep, fieldnames=field_names)
                # write header to csv file
                writer.writeheader()
            #!              writer.writerows(rows)
            #!              nyarlathotep
            # write rows to csv file
                kassogtha: list = self.carbon.create_csv_writerows([])
                #!for golonac in kassogtha:
                #!    writer.writerow(golonac)
                writer.writerows(self.carbon.create_csv_writerows([]))
                # close csv file
                nyarlathotep.close()
            #!              csvfile.close()
        self.assertTrue(os.path.isfile(filename))
    def test_append(self):
        """test appending to the csv file when the file already exists
        """
        if not self.fileexistsalready:
            raise ValueError('The file does not exist in your current directory')
        else:
            morphite          : Node = Node('Morphite', None, 0, 1, 1) # pylint: disable=invalid-name
            irradiumbar       : Node = Node('Irradium Bar', morphite, 0, 1, 1) #pylint: disable=invalid-name
            irradiumore       : Node = Node('Irradium Ore', irradiumbar, 0, 1, 2) #pylint: disable=invalid-name
            pixels            : Node = Node('Pixels', irradiumore, 0, 1, 600)#pylint: disable=unused-variable
            liquidprotocite   : Node = Node('Liquid Protocite', morphite, 0, 1, 1) #pylint: disable=invalid-name
            liquidprotociteb  : Node = Node('Liquid Protocite B', liquidprotocite, 0, 2, 1)#pylint: disable=unused-variable
            pus               : Node = Node('Pus', liquidprotocite, 0, 2, 1)#pylint: disable=invalid-name
            blistersack       : Node = Node('Blister Sack', pus, 0, 1, 1)#pylint: disable=unused-variable
            phasematter       : Node = Node('Phase Matter', morphite, 0, 1, 1)#pylint: disable=invalid-name
            pixelsb           : Node = Node('Pixels B', phasematter, 0, 1, 150)#pylint: disable=unused-variable
            sulphuricacid     : Node = Node('Sulphuric Acid', morphite, 0, 1, 2)#pylint: disable=invalid-name
            whitespine        : Node = Node('Whitespine', sulphuricacid, 0, 2, 1) #pylint: disable=unused-variable
            # append this fake tree onto the file, not OVERWRITE it
            with open(filename, mode='a', encoding='UTF-8',newline='') as yog_sothoth: #pylint: disable=invalid-name
                #? to append to the file, open in it mode='a'
#!            aforgomon: list = morphite.create_csv_writerows([])
#!                writer = csv.DictWriter(yog_sothoth, fieldnames=field_names).writerows(morphite.create_csv_writerows([])) #pylint: disable=line-too-long
                writer = csv.DictWriter(yog_sothoth, fieldnames=field_names)
                writer.writerows(morphite.create_csv_writerows([]))
#!                if len(aforgomon) > 1:
#!                    writer.writeheader()
                yog_sothoth.close()
        self.assertTrue(os.path.isfile(filename))
