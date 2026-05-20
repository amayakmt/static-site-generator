import unittest
from convert_raw import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):

    def test_nodes_to_code(self):
        nodes = [
        TextNode("This is text with a `code block` word", TextType.TEXT),
        ]

        new_nodes = [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), new_nodes)

    def test_nodes_to_bold(self):
        nodes = [
            TextNode("This is **bold** text", TextType.TEXT),
        ]

        new_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), new_nodes)

    def test_nodes_to_italic(self):
        nodes = [
            TextNode("This is _italic_ text", TextType.TEXT),
        ]

        new_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), new_nodes)

    def test_multiple_delimiters_in_one_node(self):
        nodes = [
            TextNode("a `b` c `d` e", TextType.TEXT),
        ]

        new_nodes = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.CODE),
            TextNode(" e", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), new_nodes)

    def test_multiple_text_nodes_in_input(self):
        nodes = [
            TextNode("a `b` c", TextType.TEXT),
            TextNode("d `e` f", TextType.TEXT),
        ]

        new_nodes = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" c", TextType.TEXT),
            TextNode("d ", TextType.TEXT),
            TextNode("e", TextType.CODE),
            TextNode(" f", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), new_nodes)

    def test_non_text_node_passthrough(self):
        nodes = [
            TextNode("already bold", TextType.BOLD),
        ]

        new_nodes = [
            TextNode("already bold", TextType.BOLD),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), new_nodes)

    def test_mixed_text_and_non_text_input(self):
        nodes = [
            TextNode("This is `code` here", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("and `more` text", TextType.TEXT),
        ]

        new_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("and ", TextType.TEXT),
            TextNode("more", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), new_nodes)

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_delimiter_at_end(self):
        nodes = [
            TextNode("before `code`", TextType.TEXT),
        ]

        new_nodes = [
            TextNode("before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), new_nodes)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode(
            "![logo](https://example.com/logo.png) followed by text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("logo", TextType.IMAGE, "https://example.com/logo.png"),
                TextNode(" followed by text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_consecutive_images(self):
        node = TextNode(
            "![a](https://example.com/a.png)![b](https://example.com/b.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://example.com/a.png"),
                TextNode("b", TextType.IMAGE, "https://example.com/b.png"),
            ],
            new_nodes,
        )

    def test_split_no_images(self):
        node = TextNode("Just some plain text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("Just some plain text with no images.", TextType.TEXT)],
            new_nodes,
        )

    def test_split_images_non_text_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("already bold", TextType.BOLD)],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_split_link_ignores_images(self):
        node = TextNode(
            "Mixed: ![an image](https://example.com/img.png) then a [real link](https://example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(
                    "Mixed: ![an image](https://example.com/img.png) then a ",
                    TextType.TEXT,
                ),
                TextNode("real link", TextType.LINK, "https://example.com"),
            ],
            new_nodes,
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text_no_markdown(self):
        text = "This is just plain text without any markdown."
        self.assertListEqual(
            [TextNode("This is just plain text without any markdown.", TextType.TEXT)],
            text_to_textnodes(text),
        )

    def test_only_bold(self):
        text = "This is **very bold** text"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("very bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_only_italic(self):
        text = "This is _italic_ text"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_only_code(self):
        text = "Run `npm install` first"
        self.assertListEqual(
            [
                TextNode("Run ", TextType.TEXT),
                TextNode("npm install", TextType.CODE),
                TextNode(" first", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_only_image(self):
        text = "Look at this ![cat](https://example.com/cat.png) please"
        self.assertListEqual(
            [
                TextNode("Look at this ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://example.com/cat.png"),
                TextNode(" please", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_only_link(self):
        text = "Go to [boot dev](https://www.boot.dev) now"
        self.assertListEqual(
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" now", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

    def test_bold_and_italic_mixed(self):
        text = "**bold** then _italic_ then **bold again**"
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" then ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" then ", TextType.TEXT),
                TextNode("bold again", TextType.BOLD),
            ],
            text_to_textnodes(text),
        )

    def test_image_and_link_together(self):
        text = "An ![image](https://example.com/img.png) and a [link](https://example.com) side by side"
        self.assertListEqual(
            [
                TextNode("An ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/img.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" side by side", TextType.TEXT),
            ],
            text_to_textnodes(text),
        )

if __name__ == "__main__":
    unittest.main()