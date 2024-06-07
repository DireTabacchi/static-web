import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ulist,
    block_type_olist,
    markdown_to_html_node,
)
from htmlnode import (
    ParentNode,
    LeafNode
)


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

    def test_block_type(self):
        markdown_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
            "```\n#include <stdio.h>\nint main() {\n    printf(\"Hello world\");\n}\n```",
            "> Roses are red,\n> Violets are blue,\n> One day we'll meet,\n> down Blood Gulch Avenue",
            "1. Write code\n2. ???\n3. Profit",
        ]
        expected = [
            block_type_heading,
            block_type_paragraph,
            block_type_ulist,
            block_type_code,
            block_type_quote,
            block_type_olist,
        ]
        for block, exp in zip(markdown_blocks, expected):
            self.assertEqual(exp, block_to_block_type(block))

    def test_block_type_headings(self):
        markdown_blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        expected = [
            block_type_heading,
            block_type_heading,
            block_type_heading,
            block_type_heading,
            block_type_heading,
            block_type_heading,
        ]
        for block, exp in zip(markdown_blocks, expected):
            self.assertEqual(exp, block_to_block_type(block))

    def test_block_type_malformed_headings(self):
        markdown_blocks = [
            "#Heading",
            "####### Heading",
        ]
        expected = [
            block_type_paragraph,
            block_type_paragraph,
        ]
        for block, exp in zip(markdown_blocks, expected):
            self.assertEqual(exp, block_to_block_type(block))

    def test_block_type_malformed_code(self):
        markdown_blocks = [
            "```\nprint(\"Hello world\")```",
            "``\nprint(\"Hello world\")\n```",
            "``\nprint(\"Hello world\")\n``",
        ]
        expected = [
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
        ]
        for block, exp in zip(markdown_blocks, expected):
            self.assertEqual(exp, block_to_block_type(block))

    def test_block_type_malformed_quote(self):
        markdown_blocks = [
            "> This is a test\nThis line should make this a paragraph block\n> This line means nothing",
            "forgor the >\n>This line won't be evaluated",
        ]
        expected = [
            block_type_paragraph,
            block_type_paragraph,
        ]
        for block, exp in zip(markdown_blocks, expected):
            self.assertEqual(exp, block_to_block_type(block))

    def test_block_type_malformed_ulist(self):
        markdown_blocks = [
            "* This list starts with an asterisk\n- but has a dash\n* so it will be a paragraph",
            "- This list starts with a dash\n* but has an asterisk\n- so it will be a paragraph",
            "*oops no space\n* this will be a paragraph",
            "-oops no space\n- This will be a paragraph",
            "* will this be a ulist?\n*oops no space\n* not a ulist",
            "- will this be a ulist?\n-oops no space\n- not a ulist",
            "* This is a list item\nThis is not a list item\n* This is a paragraph",
            "- This is a list item\nThis is not a list item\n- This is a paragraph",
        ]
        expected = [
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
        ]
        for block, exp in zip(markdown_blocks, expected):
            self.assertEqual(exp, block_to_block_type(block))

    def test_block_type_malformed_olist(self):
        markdown_blocks = [
            "1. This list starts with a 1\n1. but doesn't increment correctly\n2. so it will be a paragraph",
            "1. This list starts with a 1\n2. but doesn't increment correctly\n2. so it will be a paragraph",
            "1.oops no space\n2. this will be a paragraph",
            "1. will this be a olist?\n2.oops no space\n3. not a ulist",
            "1. This is a list item\nThis is not a list item\n3. This is a paragraph",
            "2. This list starts with a 2\n3. so it will be a paragraph"
        ]
        expected = [
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
            block_type_paragraph,
        ]
        for block, exp in zip(markdown_blocks, expected):
            self.assertEqual(exp, block_to_block_type(block))

    def test_markdown_to_html_node(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item

```
#include <stdio.h>
int main() {
    printf(\"Hello world\");
}
```

> Roses are red,
> Violets are blue,
> One day we'll meet,
> down Blood Gulch Avenue

1. Write code
2. ???
3. Profit
4. Making this list
5. longer to test
6. if it can take
7. more than
8. nine lines
9. of items
10. waow"""
        expected = ParentNode("div",
            [
                ParentNode("h1",
                    [LeafNode(None, "This is a heading")]
                ),
                ParentNode("p",
                    [
                        LeafNode(
                            None,
                            "This is a paragraph of text. It has some "
                        ),
                        LeafNode("b", "bold"),
                        LeafNode(None, " and "),
                        LeafNode("i", "italic"),
                        LeafNode(None, " words inside of it."),
                    ]
                ),
                ParentNode("ul",
                    [
                        ParentNode("li",
                            [LeafNode(None, "This is a list item")]
                        ),
                        ParentNode("li",
                            [LeafNode(None, "This is another list item")]
                        ),
                    ]
                ),
                ParentNode("pre",
                    [
                        ParentNode("code",
                            [
                                LeafNode(None,
                                    "#include <stdio.h>\nint main() {\nprintf(\"Hello world\");\n}"
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        )
        actual = markdown_to_html_node(text)


if __name__ == "__main__":
    unittest.main()
