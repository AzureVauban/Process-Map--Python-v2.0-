"""
Unit Testing for Issue5
"""
import unittest

from main import Node


class MyUnitTest(unittest.testcase):
    testkey: str = Node.generate_treekey()
    self.assertTrue(isinstance(testkey, str))
