import unittest

from htmlnode import LeafNode
from htmlnode import ParentNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_multiple_children(self):
        parent = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " normal "),
                LeafNode("i", "italic"),
            ]
        )

        self.assertEqual(
            parent.to_html(),
            "<p><b>Bold</b> normal <i>italic</i></p>"
        )

    def test_parent_with_props(self):
        parent = ParentNode(
            "a",
            [LeafNode(None, "Click me!")],
            {"href": "https://google.com"}
        )

        self.assertEqual(
            parent.to_html(),
            '<a href="https://google.com">Click me!</a>'
        )

    def test_no_tag(self):
        parent = ParentNode(None, [LeafNode("p", "text")])

        with self.assertRaises(ValueError):
            parent.to_html()

    def test_no_children(self):
        parent = ParentNode("div", None)

        with self.assertRaises(ValueError):
            parent.to_html()


if __name__ == "__main__":
    unittest.main()