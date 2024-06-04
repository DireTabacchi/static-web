class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        prop_string = ""
        if self.props == None:
            return prop_string
        for prop, value in self.props.items():
            prop_string += f' {prop}="{value}"'
        return prop_string

    def __repr__(self):
        rep_string = "HTMLNode("
        rep_string += f"tag: {self.tag}, "
        rep_string += f"value: {self.value}, "
        rep_string += f"children: "
        if self.children == None:
            rep_string += "None, "
        else:
            rep_string += "["
            for i in range(len(self.children)):
                rep_string += f"{self.children[i].tag}"
                rep_string += ", " if i < len(self.children) - 1 else "], "
        rep_string += f"props: {self.props})"
        return rep_string

