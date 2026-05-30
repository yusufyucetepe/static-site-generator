import unittest
from textnode import TextNode, TextType, text_node_to_html_node

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

if __name__ == "__main__":
    unittest.main()