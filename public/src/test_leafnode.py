import unittest
from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_leaf_failure(self):
        node = LeafNode("p", "Well hay there!")
        self.assertNotEqual(node.to_html(), "p Well hay there! /p")

    def test_two_are_not_made_the_same(self):
        node = LeafNode("a", "Hi!", {"href": "http://hi.com"})
        node2 = LeafNode("a", "Hi!", {"href": "http://hi.com"})
        self.assertNotEqual(node, node2)