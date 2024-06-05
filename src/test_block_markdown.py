import unittest

from block_markdown import markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        actual = markdown_to_blocks(text)
        self.assertListEqual(expected, actual)

    def test_markdown_to_blocks_2(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ]
        actual = markdown_to_blocks(text)
        self.assertListEqual(expected, actual)

    def test_markdown_to_blocks_extra_newlines(self):
        text = """# This is a heading



This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ]
        actual = markdown_to_blocks(text)
        self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
