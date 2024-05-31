import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_content_neq(self):
        node = TextNode("Three cups", "italic")
        node2 = TextNode("Four cups", "italic")
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("1/2 kg", "bold")
        node2 = TextNode("1/2 kg", "italic")
        self.assertNotEqual(node, node2)

    def test_populated_url(self):
        node = TextNode("get help", "link", "http://www.help.com")
        node2 = TextNode("get help", "link", "http://www.help.com")
        self.assertEqual(node, node2)

    def test_url_no_url(self):
        node = TextNode("get help", "link")
        node2 = TextNode("get help", "link", "http://www.help.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
