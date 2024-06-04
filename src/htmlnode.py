class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        prop_string = ""
        for prop, value in self.props.items():
            prop_string += f' {prop}="{value}"'
        return prop_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: no value")
        if self.tag == None:
            return self.value
        # create the opening tag
        open_tag = "<" + self.tag + self.props_to_html() + ">"
        close_tag = "</" + self.tag + ">"
        return open_tag + self.value + close_tag

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
