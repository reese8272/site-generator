import unittest
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node
from split_nodes import split_nodes_delimiter
from regex import extract_markdown_images, extract_markdown_links


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold value", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold value")

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, url = "1234.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props["href"], "1234.com")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, url = "123.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props['src'], "123.png")
        self.assertEqual(html_node.props['alt'], "This is an image")


class TestDelimiterSplit(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "This is text with a "
        assert new_nodes[0].text_type == TextType.TEXT
        assert new_nodes[1].text == "code block"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " word"
        assert new_nodes[2].text_type == TextType.TEXT
    
    def test_split_nodes_delimiter_multiple(self):
        node = TextNode("This `code` has `multiple` code blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 5
        assert new_nodes[0].text == "This "
        assert new_nodes[1].text == "code"
        assert new_nodes[1].text_type == TextType.CODE
        assert new_nodes[2].text == " has "
        assert new_nodes[3].text == "multiple"
        assert new_nodes[3].text_type == TextType.CODE
        assert new_nodes[4].text == " code blocks"
    
    def test_split_nodes_delimiter_edge_positions(self):
        node = TextNode("`code` at beginning and end `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        assert len(new_nodes) == 3
        assert new_nodes[0].text == "code"
        assert new_nodes[0].text_type == TextType.CODE
        assert new_nodes[1].text == " at beginning and end "
        assert new_nodes[1].text_type == TextType.TEXT
        assert new_nodes[2].text == "code"
        assert new_nodes[2].text_type == TextType.CODE


class TestRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_images_string_valid(self):
        matches = extract_markdown_images("Here's an ![logo](https://example.com/logo.png)")
        self.assertListEqual([("logo", "https://example.com/logo.png")], matches)

    def test_extract_images_list_valid(self):
        matches = extract_markdown_images([
            "Header image: ![header](https://img.com/header.jpg)",
            "Icon: ![icon](https://img.com/icon.png)"
        ])
        self.assertListEqual([
            ("header", "https://img.com/header.jpg"),
            ("icon", "https://img.com/icon.png")
        ], matches)

    def test_extract_images_invalid_input(self):
        with self.assertRaises(Exception) as context:
            extract_markdown_images(12345)
        self.assertIn("Error, invalid type passed", str(context.exception))


    def test_extract_links_string_valid(self):
        matches = extract_markdown_links("Click [here](https://boot.dev)")
        self.assertListEqual([("here", "https://boot.dev")], matches)

    def test_extract_links_list_valid(self):
        matches = extract_markdown_links([
            "Visit [site](https://example.com)",
            "More info at [docs](https://example.com/docs)"
        ])
        self.assertListEqual([
            ("site", "https://example.com"),
            ("docs", "https://example.com/docs")
        ], matches)

    def test_extract_links_malformed(self):
        matches = extract_markdown_links("Broken link: [broken](missing-end")
        self.assertListEqual([], matches)


if __name__ == "__main__":
    unittest.main()