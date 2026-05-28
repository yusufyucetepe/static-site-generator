import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()