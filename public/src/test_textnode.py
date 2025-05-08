import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node3)

        node4 = TextNode("This is a text node", TextType.BOLD, url = "12345.com")
        node5 = TextNode("This is a text node", TextType.BOLD, url = "12345.com")
        self.assertEqual(node4, node5)

        node6 = TextNode("This is a text node", TextType.BOLD, url = "56789.com")
        self.assertNotEqual(node4, node6)
        self.assertNotEqual(node, node6)


if __name__ == "__main__":
    unittest.main()