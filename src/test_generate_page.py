import unittest
from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_basic(self):
        self.assertEqual(extract_title("# Hello world"), "Hello world")

    def test_extract_title_in_document(self):
        md = "Some intro text.\n\n# The Title\n\nMore content."
        self.assertEqual(extract_title(md), "The Title")

    def test_extract_title_strips_trailing_whitespace(self):
        self.assertEqual(extract_title("# Title   "), "Title")

    def test_extract_title_ignores_h2_and_below(self):
        md = "## Subtitle\n\n### Smaller heading"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_no_title_raises(self):
        md = "Just a paragraph.\n\nAnother one."
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_extract_title_empty_string_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_extract_title_returns_first_h1(self):
        md = "# First Title\n\nSome text.\n\n# Second Title"
        self.assertEqual(extract_title(md), "First Title")


if __name__ == "__main__":
    unittest.main()
