import unittest

from htmlnode import ParentNode, LeafNode


class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        test_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text")
            ],
        )
        self.assertEqual(test_node.value, None)

    def test_to_html(self):
        test_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text")
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>"
        self.assertEqual(expected, test_node.to_html())

    def test_to_html_nested_parents(self):
        node = ParentNode(
            "p",
            [
                LeafNode(None, "If you are stuck, "),
                ParentNode(
                    "b",
                    [
                        LeafNode("a", "rtfm", {"href": "https://docs.python.org/3/"}),
                    ],
                ),
                LeafNode(None, ". That's all there is to it."),
            ],
        )
        expected = '<p>If you are stuck, <b><a href="https://docs.python.org/3/">rtfm</a></b>. That\'s all there is to it.</p>'
        self.assertEqual(expected, node.to_html())


if __name__ == "__main__":
    unittest.main()
