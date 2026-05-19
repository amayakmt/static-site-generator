
class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict = None
        ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError('not implemented in a parent node: HTMLNode')

    def props_to_html(self):
        if self.props:
            return "".join(f' {key}="{value}"' for key, value in self.props.items())
        return ""

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str | None,
        props: dict = None
        ):
        super().__init__(tag, value, children=None, props=props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError('a leaf node must have a value')
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'LeafNode({self.tag}, {self.value}, {self.props})'

class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict = None
        ):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("a parent node must have a tag")
        if self.children is None:
            raise ValueError("a parent node must have children")

        substring = ""
        for child in self.children:
            substring += child.to_html()
        
        return f'<{self.tag}{self.props_to_html()}>{substring}</{self.tag}>'

            