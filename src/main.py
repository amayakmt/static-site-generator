from textnode import TextNode, TextType

dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

print(repr(dummy))