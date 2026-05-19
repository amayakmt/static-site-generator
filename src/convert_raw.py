from textnode import TextNode, TextType

def split_nodes_delimiter(
    old_nodes: list["TextNode"],
    delimiter: str,
    text_type: TextType
    ) -> list["TextNode"]:
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        elif delimiter not in node.text:
            raise Exception(f'delimiter {delimiter} not found in node: {node.text}')

        split_texts = node.text.split(delimiter)
        for text in split_texts:
            if text == "":
                continue
            if text != text.strip():
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes
