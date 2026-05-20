from textnode import TextNode, TextType
from extract_md_objects import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(
    old_nodes: list["TextNode"],
    delimiter: str,
    text_type: TextType
    ) -> list["TextNode"]:
    
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
            continue
            
        split_texts = node.text.split(delimiter)

        if len(split_texts) % 2 == 0:
            raise ValueError(f'the delimiter "{delimiter}" is unbalanced: {node.text}')

        for idx, text in enumerate(split_texts):
            if text == "":
                continue
            if idx % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))

    return new_nodes

def split_nodes_image(old_nodes: list["TextNode"]) -> list["TextNode"]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        for alt, url in extract_markdown_images(node.text):
            before, remaining = remaining.split(f"![{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        remaining = node.text
        for alt, url in extract_markdown_links(node.text):
            before, remaining = remaining.split(f"[{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes