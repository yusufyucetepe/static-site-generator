import unittest
from markdown_utils import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Spaced Title  "), "Spaced Title")

    def test_ignores_h2(self):
        self.assertEqual(extract_title("## Not a title\n# Actual Title"), "Actual Title")

    def test_multiline_markdown(self):
        md = "# My Page\n\nSome paragraph text."
        self.assertEqual(extract_title(md), "My Page")

    def test_no_h1_raises(self):
        with self.assertRaises(Exception):
            extract_title("## Only an h2 here")

    def test_empty_raises(self):
        with self.assertRaises(Exception):
            extract_title("")


if __name__ == "__main__":
    unittest.main()
