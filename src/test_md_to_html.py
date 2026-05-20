import unittest
from md_to_html import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        md = "This is **bolded** paragraph text"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text</p></div>",
        )

    def test_multiple_paragraphs(self):
        md = "First paragraph here.\n\nSecond paragraph with _italic_."
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph here.</p><p>Second paragraph with <i>italic</i>.</p></div>",
        )

    def test_heading_h1(self):
        md = "# Hello world"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h1>Hello world</h1></div>")

    def test_heading_h6(self):
        md = "###### Deepest heading"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(html, "<div><h6>Deepest heading</h6></div>")

    def test_heading_with_inline_markdown(self):
        md = "## Has **bold** and _italic_"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h2>Has <b>bold</b> and <i>italic</i></h2></div>",
        )

    def test_code_block(self):
        md = "```\nprint('hi')\nx = 5\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>print('hi')\nx = 5\n</code></pre></div>",
        )

    def test_code_block_no_inline_parsing(self):
        md = "```\nthis **is not** bold inside code\n```"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>this **is not** bold inside code\n</code></pre></div>",
        )

    def test_quote(self):
        md = "> first line\n> second line"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>first line second line</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- apple\n- banana\n- cherry"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>apple</li><li>banana</li><li>cherry</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_ordered_list_double_digit(self):
        md = "\n".join(f"{i}. item {i}" for i in range(1, 11))
        html = markdown_to_html_node(md).to_html()
        expected_items = "".join(f"<li>item {i}</li>" for i in range(1, 11))
        self.assertEqual(html, f"<div><ol>{expected_items}</ol></div>")

    def test_list_with_inline_markdown(self):
        md = "- **bold** item\n- _italic_ item\n- a `code` item"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li><li>a <code>code</code> item</li></ul></div>",
        )

    def test_paragraph_with_link_and_image(self):
        md = "Visit [boot dev](https://www.boot.dev) and see ![logo](https://example.com/logo.png)"
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><p>Visit <a href="https://www.boot.dev">boot dev</a> and see <img src="https://example.com/logo.png" alt="logo"></img></p></div>',
        )

    def test_mixed_document(self):
        md = """# Title

Some **bold** text in a paragraph.

- list item 1
- list item 2

> A quoted line"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div>"
            "<h1>Title</h1>"
            "<p>Some <b>bold</b> text in a paragraph.</p>"
            "<ul><li>list item 1</li><li>list item 2</li></ul>"
            "<blockquote>A quoted line</blockquote>"
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()
