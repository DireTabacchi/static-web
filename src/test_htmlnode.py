import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_error(self):
        test_node = HTMLNode("p", "Hello world")
        self.assertRaises(NotImplementedError, test_node.to_html)

    def test_repr_value_no_children(self):
        test_node = HTMLNode("p", "Hello world")
        expected_value = "HTMLNode(tag: p, value: Hello world, children: None, props: None)"
        print('\nTesting: HTMLNode("p", "Hello world")')
        print(f"Expected value:\n{expected_value}")
        print(f"Actual value:\n{test_node}")
        print("======================================================================")
        self.assertEqual(test_node.__repr__(), expected_value)

    def test_props_to_html(self):
        test_node = HTMLNode("a", "Hello world", None, {"href": "google.com", "target": "_blank"})
        expected_value = ' href="google.com" target="_blank"'
        print("\nTesting: props_to_html")
        print('Given value: HTMLNode("a", "Hello world", None, {"href": "google.com", "target": "_blank"})')
        print(f"Expected value:\n{expected_value}")
        print(f"Actual value:\n{test_node.props_to_html()}")
        print("======================================================================")
        self.assertEqual(test_node.props_to_html(), expected_value)
        
    def test_no_props_to_html(self):
        test_node = HTMLNode("p", "Hello world")
        expected_value = ''
        self.assertEqual(test_node.props_to_html(), expected_value)

    def test_repr_children_no_value(self):
        child1 = HTMLNode("li", "code")
        child2 = HTMLNode("li", "???")
        child3 = HTMLNode("li", "profit")
        test_node = HTMLNode("ol", None, [child1, child2, child3])
        expected_value = "HTMLNode(tag: ol, value: None, children: [li, li, li], props: None)"
        print('\nTesting: HTMLNode("ol", None, [child1, child2, child3])')
        print(f"Expected value:\n{expected_value}")
        print(f"Actual value:\n{test_node}")
        print("======================================================================")
        self.assertEqual(test_node.__repr__(), expected_value)
