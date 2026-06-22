from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    result = []

    for block in blocks:
        block = block.strip()

        if block:
            result.append(block)

    return result

def block_to_block_type(block):
    lines = block.split("\n")

    # Heading
    for i in range(1, 7):
        if block.startswith("#" * i + " "):
            return BlockType.HEADING

    # Code
    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE

    # Quote
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break

    if is_quote:
        return BlockType.QUOTE

    # Unordered list
    is_ul = True
    for line in lines:
        if not line.startswith("- "):
            is_ul = False
            break

    if is_ul:
        return BlockType.UNORDERED_LIST

    # Ordered list
    is_ol = True

    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            is_ol = False
            break

    if is_ol:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
