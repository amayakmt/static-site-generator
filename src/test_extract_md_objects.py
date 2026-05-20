import unittest
from extract_md_objects import extract_markdown_images, extract_markdown_links


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) "
            "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_single_image(self):
        text = "Just one ![cat](https://example.com/cat.png) here."
        self.assertEqual(
            extract_markdown_images(text),
            [("cat", "https://example.com/cat.png")],
        )

    def test_extract_no_images(self):
        text = "This is plain text with no images at all."
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_image_empty_alt(self):
        text = "An image with no alt: ![](https://example.com/img.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("", "https://example.com/img.png")],
        )

    def test_extract_image_with_query_url(self):
        text = "Image with query params: ![photo](https://cdn.example.com/img.jpg?w=200&h=300)"
        self.assertEqual(
            extract_markdown_images(text),
            [("photo", "https://cdn.example.com/img.jpg?w=200&h=300")],
        )

    def test_extract_images_ignores_links(self):
        text = (
            "Has both: [a link](https://example.com) and "
            "![an image](https://example.com/img.png)"
        )
        self.assertEqual(
            extract_markdown_images(text),
            [("an image", "https://example.com/img.png")],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links(self):
        text = (
            "This is text with a link [to boot dev](https://www.boot.dev) "
            "and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_single_link(self):
        text = "Just one [click here](https://example.com) link."
        self.assertEqual(
            extract_markdown_links(text),
            [("click here", "https://example.com")],
        )

    def test_extract_no_links(self):
        text = "This is plain text with no links at all."
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_link_empty_text(self):
        text = "A link with no text: [](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("", "https://example.com")],
        )

    def test_extract_links_ignores_images(self):
        text = (
            "Mixed content: ![an image](https://example.com/img.png) "
            "and a real [link](https://example.com)"
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("link", "https://example.com")],
        )


if __name__ == "__main__":
    unittest.main()
