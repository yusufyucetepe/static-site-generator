import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_no_value(self):
            node = LeafNode("p", None)

            with self.assertRaises(ValueError):
                node.to_html()

    def test_leaf_raw_text(self):
            node = LeafNode(None, "Raw text")

            self.assertEqual(
                node.to_html(),
                "Raw text"
            )

if __name__ == "__main__":
    unittest.main()
