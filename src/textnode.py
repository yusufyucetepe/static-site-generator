import re
from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            "img",
            "",
            {
                "src": text_node.url,
                "alt": text_node.text,
            },
        )

    raise Exception("Invalid TextType")

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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    result = []

    for block in blocks:
        block = block.strip()

        if block:
            result.append(block)

    return result