from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, split_nodes_images, split_nodes_links

def text_to_textnodes(text):
    result = [TextNode(text, TextType.TEXT)]

    delimiters = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE)
    ]
    
    # Apply each delimiter splitting function
    for delimiter, text_type in delimiters:
        result = split_nodes_delimiter(result, delimiter, text_type)
    
    # After handling basic delimiters, process images and links
    result = split_nodes_images(result)
    result = split_nodes_links(result)


    return result
    