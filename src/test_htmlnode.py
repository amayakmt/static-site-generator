import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode(self):
        prop = {
            "href": "https://www.google.com",
            "target": "_blank",
            }
        node = HTMLNode("p", "hello world")
        node2 = HTMLNode("code", "print('hello world')")
        node3 = HTMLNode("blockquote", "This is a quote.")
        node4 = HTMLNode("li", "Item 1")
        node5 = HTMLNode("p", "bold text", None, prop)
        
        self.assertEqual(node5.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node4.props_to_html(), '')
        self.assertEqual(node3.props_to_html(), '')

if __name__ == "__main__":
    unittest.main()
