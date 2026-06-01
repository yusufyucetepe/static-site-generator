import unittest
from textnode import TextNode, TextType
from textnode import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links

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

if __name__ == "__main__":
    unittest.main()