import unittest
from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multiple_children(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                LeafNode(None, " and "),
                LeafNode("i", "italic"),
                LeafNode(None, " text."),
            ],
        )
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold</b> and <i>italic</i> text.</p>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode(None, "click me")
        parent_node = ParentNode(
            "a",
            [child_node],
            {"href": "https://example.com", "target": "_blank"},
        )
        self.assertEqual(
            parent_node.to_html(),
            '<a href="https://example.com" target="_blank">click me</a>',
        )

    def test_to_html_no_tag_raises(self):
        parent_node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()