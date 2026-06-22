import re
from enum import Enum
from textnode import TextNode, TextType

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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"Invalid markdown syntax: unmatched {delimiter}")

        for i in range(len(parts)):
            if parts[i] == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(
        r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",
        text,
    )


def extract_markdown_links(text):
    return re.findall(
        r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",
        text,
    )

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        images = extract_markdown_images(text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for alt, url in images:
            sections = text.split(f"![{alt}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown image")

            if sections[0]:
                new_nodes.append(
                    TextNode(sections[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(alt, TextType.IMAGE, url)
            )

            text = sections[1]

        if text:
            new_nodes.append(
                TextNode(text, TextType.TEXT)
            )

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for anchor, url in links:
            sections = text.split(f"[{anchor}]({url})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown link")

            if sections[0]:
                new_nodes.append(
                    TextNode(sections[0], TextType.TEXT)
                )

            new_nodes.append(
                TextNode(anchor, TextType.LINK, url)
            )

            text = sections[1]

        if text:
            new_nodes.append(
                TextNode(text, TextType.TEXT)
            )

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(
        nodes,
        "**",
        TextType.BOLD,
    )
    nodes = split_nodes_delimiter(
        nodes,
        "_",
        TextType.ITALIC,
    )
    nodes = split_nodes_delimiter(
        nodes,
        "`",
        TextType.CODE,
    )

    return nodes