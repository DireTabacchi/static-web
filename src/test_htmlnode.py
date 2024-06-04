import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_error(self):
        test_node = HTMLNode("p", "Hello world")
        self.assertRaises(NotImplementedError, test_node.to_html)

    def test_no_props_to_html(self):
        test_node = HTMLNode("p", "Hello world")
        expected_value = ''
        self.assertEqual(test_node.props_to_html(), expected_value)
