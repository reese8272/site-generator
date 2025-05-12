from enum import Enum


class TextType(Enum):
    '''
    and enum class that ensured we create a text type that
        is compliant with html types
    '''
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    '''
    The text node class that has the text, the type, and an optional URL.
    This ensures that each text is treated uniformly.
    We are simply caputuring the common attributes that our generator recognizes.
    '''
    def __init__(self, text, text_type, url=None):
        # text and text_type are required, or else it's not a *real* text node
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        '''
        ensured that we can do something like node1 == node2 with a true or false
        '''
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        '''
        So that we can print node1 without returning it's object pointer.
        Also, this is good for debugging purposes, and is better represented
            than say __str__.
        '''
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"