from textnode import TextType
from htmlnode import LeafNode
import re

def text_node_to_html_node(text_node):
    '''
    This method essentially creates our Leaf Nodes based off the text_type given from the
        text node file and the TextNode class
    '''
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag = None, value = text_node.text)
        case TextType.BOLD:
            return LeafNode(tag = "b", value = text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag = "i", value = text_node.text)
        case TextType.CODE:
            return LeafNode(tag = "code", value = text_node.text)
        case TextType.LINK:
            return LeafNode(tag = "a", value = text_node.text, props={"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode(tag = "img", value = "", props = {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Invalid TextNode format.")
        

def markdown_to_blocks(markdown):
    new_markdown = re.split(r"\n{2,}", markdown)
    return list(filter(lambda x: x, map(str.strip, new_markdown)))

if __name__ == "__main__":
    markdown = """
    This is a markdown text
    with multiple lines

    -bullet
    -bullet

    1) number
    2) numer
    """

    print(markdown_to_blocks(markdown))