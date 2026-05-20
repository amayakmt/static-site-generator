import unittest
from split_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
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

    def test_single_block(self):
        md = "Just one paragraph, no blank lines."
        self.assertEqual(
            markdown_to_blocks(md),
            ["Just one paragraph, no blank lines."],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        md = "   \n\n   \n\n\t\n"
        self.assertEqual(markdown_to_blocks(md), [])

    def test_excessive_blank_lines(self):
        md = "first block\n\n\n\nsecond block\n\n\n\n\nthird block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["first block", "second block", "third block"],
        )

    def test_trims_block_whitespace(self):
        md = "   leading spaces\n\ntrailing spaces   \n\n   both sides   "
        self.assertEqual(
            markdown_to_blocks(md),
            ["leading spaces", "trailing spaces", "both sides"],
        )

    def test_preserves_internal_newlines(self):
        md = "line one\nline two\nline three\n\nnext block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["line one\nline two\nline three", "next block"],
        )

    def test_heading_and_list_blocks(self):
        md = "# Heading\n\n- item 1\n- item 2\n- item 3\n\nA closing paragraph."
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# Heading",
                "- item 1\n- item 2\n- item 3",
                "A closing paragraph.",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_h1(self):
        self.assertEqual(
            block_to_block_type("# Hello world"),
            BlockType.HEADING,
        )

    def test_heading_h6(self):
        self.assertEqual(
            block_to_block_type("###### Deepest heading"),
            BlockType.HEADING,
        )

    def test_heading_too_many_hashes(self):
        self.assertEqual(
            block_to_block_type("####### Seven hashes is not a heading"),
            BlockType.PARAGRAPH,
        )

    def test_heading_no_space_after_hashes(self):
        self.assertEqual(
            block_to_block_type("#NoSpace"),
            BlockType.PARAGRAPH,
        )

    def test_heading_only_hashes(self):
        self.assertEqual(
            block_to_block_type("###"),
            BlockType.PARAGRAPH,
        )

    def test_code_block(self):
        block = "```\nprint('hello')\nprint('world')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE,
        )

    def test_code_block_missing_opening_newline(self):
        block = "```python\nprint('hello')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_quote_single_line(self):
        self.assertEqual(
            block_to_block_type("> a single quoted line"),
            BlockType.QUOTE,
        )

    def test_quote_multiline(self):
        block = "> first line\n> second line\n>third line without space"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE,
        )

    def test_quote_with_one_non_quote_line(self):
        block = "> first line\nthis line breaks the quote"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list_single_item(self):
        self.assertEqual(
            block_to_block_type("- only one item"),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_multiple_items(self):
        block = "- apple\n- banana\n- cherry"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_missing_space(self):
        block = "-apple\n-banana"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_well_formed(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_starts_at_two(self):
        block = "2. wrong start\n3. continues"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_skips_number(self):
        block = "1. first\n3. skipped two"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_double_digit_numbers(self):
        block = "\n".join(f"{i}. item {i}" for i in range(1, 11))
        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_paragraph_plain_text(self):
        self.assertEqual(
            block_to_block_type("This is just a regular paragraph."),
            BlockType.PARAGRAPH,
        )

    def test_paragraph_with_inline_markdown(self):
        block = "This has **bold**, _italic_, and `code` but no block-level markers."
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
