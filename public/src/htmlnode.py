class HTMLNode:
    '''
    The main Node for the Static Site Generator Project.
    [args]:
        tag =  where we need to say if its a paragraph (p), bold (b), or a div.
        value = the main text of the node, what is actually outputted onto the screen
        children = any rooted nodes that also have tags, value, and props
        props = anything such as references, hyperlinks, or anything of that sort
    '''
    def __init__(self, tag=None, value=None, children=None, props=None):
        '''
        Constructor method, all values are optional in an HTML Node for best handling (makes our jobs easier essentially)
        '''
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        '''
        This method is used in child classes to turn their node into the correct type of HTML format.
        '''
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        '''
        Turns the props that we were talking about into the proper html format.
        Once we understand that the props is just a dictionary (and not nested),
            we can iterate over the props and do the proper html format of:
            "prop = 'prop attribute here'"
            and finall append that to a long string of the props
        '''
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        '''
        we have this to properly print the HTML node whenever we need to see the attributes,
            instead of seeing that <x Object at alkvnas> or whatever.
        '''
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    '''
    Child class of HTML Node, this assumes no children, tags and values are a MUST,
        and props are optional. We MUST have a tag and a value for proper HTML format,
        as well as to avoid errors and edge cases
    '''
    def __init__(self, tag, value, props = None):
        '''
        Constructor method, as mentioned before, NO children
        '''
        super().__init__(tag = tag, value = value, children = None, props = props)

    def to_html(self):
        '''
        to_html called here, checks to ensure there is a value or else it will raise an error.
        We return the str(self.value) if the tag is none because that means that what we have for
            our leaf node is raw text, therefore return the str of our value
        '''
        if self.value is None:
            raise ValueError("No Value in Node")
        if self.tag is None:
            return str(self.value)
        
        # this makes sense, because we want to take the props of the leaf node (that we node is the last node of a nested tree)
        #   and convert it to the proper html formatting
        props_str = self.props_to_html()

        # this now makes more sense! The way to format HTML is <tag><any props><the actual text></tag>
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    '''
    Child class of HTML Node. Tag and children are required because they are assumed to not be the final node,
        thus there MUST be a child in order for it to be called a parent node.
    No text because the leaf nodes contain the text
    Again, props is optional
    '''
    def __init__(self, tag, children, props = None):
        '''
        Constructor that only asks for tags, children, and props (but props is the only one with a default value of None)
        '''
        super().__init__(tag = tag, children = children, props = props)

    def to_html(self):
        # Checks to ensure that we have a tag and children, or else it will raise an error
        if self.tag is None:
            raise ValueError("No tag found. Tag is needed.")
        if self.children is None:
            raise ValueError("No children found. Children is needed.")
        
        # HOW THE RECURSION WORKS:
        # the starting tag of our current node, any props converted to html,
        #   and then iterating over each child in our current node, doing the same return of tag and props,
        #   and then joining them with '' or else we'd be returning a list, and then all of them are enclosed
        #   with a closing </tag>
        # while the initial code was confusing, it makes sense now to see the recursion in action and
        # genuinely going over and rereading it
        return f"<{self.tag}{self.props_to_html()}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"