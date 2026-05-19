import unittest
from convert_raw import split_nodes_delimiter
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

    def test_no_delimiter_raises(self):
        nodes = [
            TextNode("plain text with no delimiter", TextType.TEXT),
        ]

        with self.assertRaises(Exception):
            split_nodes_delimiter(nodes, "`", TextType.CODE)

    def test_delimiter_at_end(self):
        nodes = [
            TextNode("before `code`", TextType.TEXT),
        ]

        new_nodes = [
            TextNode("before ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), new_nodes)

if __name__ == "__main__":
    unittest.main()