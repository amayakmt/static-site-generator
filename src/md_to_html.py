from split_blocks import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from convert_raw import text_to_textnodes
from textnode import TextNode, TextType

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return list(map(TextNode.text_node_to_html_node, text_nodes))

def heading_to_node(block):
    count = 0
    while block[count] == "#":
        count += 1
    inline = block[count + 1:]
    return ParentNode(f"h{count}", text_to_children(inline))

def code_to_node(block):
    content = block[4:-3]
    text_node = TextNode(content, TextType.TEXT)
    code_leaf = TextNode.text_node_to_html_node(text_node)
    code = ParentNode("code", [code_leaf])
    return ParentNode("pre", [code])

def quote_to_node(block):
    lines = []
    for line in block.split('\n'):
        if line.startswith("> "):
            lines.append(line[2:])
        else:
            lines.append(line[1:])
    inline = " ".join(lines)
    return ParentNode("blockquote", text_to_children(inline))

def ul_to_node(block):
    items = []
    for line in block.split('\n'):
        inline = line[2:]
        items.append(ParentNode("li", text_to_children(inline)))
    return ParentNode("ul", items)

def ol_to_node(block):
    items = []
    for line in block.split('\n'):
        inline = line.split('. ', 1)[1]
        items.append(ParentNode("li", text_to_children(inline)))
    return ParentNode("ol", items)

def paragraph_to_node(block):
    return ParentNode("p", text_to_children(block))

def markdown_to_html_node(markdown) -> ParentNode:
    children = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.HEADING:
                children.append(heading_to_node(block))
            case BlockType.CODE:
                children.append(code_to_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(ul_to_node(block))
            case BlockType.ORDERED_LIST:
                children.append(ol_to_node(block))
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_node(block))
    return ParentNode("div", children)