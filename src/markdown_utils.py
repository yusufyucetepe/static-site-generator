from enum import Enum
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes

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

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children
 
 
def heading_to_html_node(block):
    level = 0
    for ch in block:
        if ch == "#":
            level += 1
        else:
            break
    text = block[level + 1:]  # skip the "### " prefix (hashes + one space)
    return ParentNode(f"h{level}", text_to_children(text))
 
 
def code_to_html_node(block):
    inner = block[4:-3]
    # text_node_to_html_node is used directly — no inline parsing
    text_node = TextNode(inner, TextType.TEXT)
    code_node = ParentNode("code", [text_node_to_html_node(text_node)])
    return ParentNode("pre", [code_node])
 
 
def quote_to_html_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        stripped_lines.append(line.lstrip(">").strip())
    content = " ".join(stripped_lines)
    return ParentNode("blockquote", text_to_children(content))
 
 
def unordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]  # strip the "- " prefix
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ul", items)
 
 
def ordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line.split(". ", 1)[1]  # strip the "N. " prefix
        items.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", items)
 
 
def paragraph_to_html_node(block):
    lines = block.split("\n")
    text = " ".join(lines)
    return ParentNode("p", text_to_children(text))
 
 
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
 
    for block in blocks:
        block_type = block_to_block_type(block)
 
        if block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children.append(unordered_list_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        else:
            children.append(paragraph_to_html_node(block))
 
    return ParentNode("div", children)