from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def markdown_to_blocks(text):
    blocks = [block.strip() for block in text.split('\n\n') if block.strip() != ""]
    return blocks

def block_to_block_type(block: str) -> BlockType:
    block_lines = block.split('\n')

    # Heading Block
    count = 0
    while count < len(block) and block[count] == "#":
        count += 1
    
    if 0 < count < 7 and count < len(block):
        if block[count] == " ":
            return BlockType.HEADING

    # Code Block
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    # Quote Block | Unordered List | Ordered List | Paragraph
    is_quote = True
    is_unordered_list = True
    is_ordered_list = True

    for idx, line in enumerate(block_lines, start=1):
        if not line.startswith('>'):
            is_quote = False
        if not line.startswith('- '):
            is_unordered_list = False
        if not line.startswith(f"{idx}. "):
            is_ordered_list = False

    if is_quote:
        return BlockType.QUOTE
    elif is_unordered_list:
        return BlockType.UNORDERED_LIST
    elif is_ordered_list:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH