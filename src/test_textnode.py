import unittest
from textnode import TextNode, TextType
from textnode import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import markdown_to_blocks

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("some text", TextType.BOLD, "https://example.com")
        node2 = TextNode("some text", TextType.BOLD, "https://example.com")
        self.assertEqual(node, node2)

    def test_different_url(self):
        node = TextNode("some text", TextType.BOLD, "https://example.com")
        node2 = TextNode("some text", TextType.BOLD, "https://other.com")
        self.assertNotEqual(node, node2)
    

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")


    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")


    def test_link(self):
        node = TextNode(
            "Google",
            TextType.LINK,
            "https://google.com"
        )
        html_node = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://google.com")

    def test_code(self):
        node = TextNode(
            "This is `code` text",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE
        )

        assert result == [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

    def test_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT
        )

        result = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD
        )

        assert result == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![one](url1) and ![two](url2)"
        )

        self.assertListEqual(
            [("one", "url1"), ("two", "url2")],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "[Boot.dev](https://www.boot.dev)"
        )

        self.assertListEqual(
            [("Boot.dev", "https://www.boot.dev")],
            matches,
        )

    def test_split_single_image(self):
        node = TextNode(
            "hello ![img](url)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "url"),
            ],
            split_nodes_image([node]),
        )

    def test_split_single_link(self):
        node = TextNode(
            "go to [google](https://google.com)",
            TextType.TEXT,
        )

        self.assertListEqual(
            [
                TextNode("go to ", TextType.TEXT),
                TextNode(
                    "google",
                    TextType.LINK,
                    "https://google.com",
                ),
            ],
            split_nodes_link([node]),
        )

    def test_text_to_textnodes(self):
        text = (
            "This is **text** with an _italic_ word and a "
            "`code block` and an "
            "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
            "and a [link](https://boot.dev)"
        )

        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode(
                    "link",
                    TextType.LINK,
                    "https://boot.dev",
                ),
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
if __name__ == "__main__":
    unittest.main()