import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_no_children(self):
        test_node = LeafNode("p", "Hello world!")
        self.assertEqual(test_node.children, None)

    def test_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node1_expected = "<p>This is a paragraph of text.</p>"
        node2_expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node1_expected, node1.to_html())
        self.assertEqual(node2_expected, node2.to_html())

    def test_to_html_no_tag(self):
        test_node = LeafNode(None, "This is raw text")
        expected = "This is raw text"
        self.assertEqual(expected, test_node.to_html())
