import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import (
    TextNode, 
    text_type_text,
    text_type_code,
    text_type_italic,
    text_type_bold,
    text_type_image,
    text_type_link,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word.", text_type_text)
        expected = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word.", text_type_text),
        ]
        self.assertListEqual(expected, split_nodes_delimiter([node], "`", text_type_code))

    def test_delim_bold(self):
        node = TextNode("This has a **bold** word in it.", text_type_text)
        expected = [
            TextNode("This has a ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word in it.", text_type_text),
        ]
        self.assertListEqual(expected, split_nodes_delimiter([node], "**", text_type_bold))

    def test_delim_many_bold(self):
        node = TextNode("The **word** is important **because it is**.", text_type_text)
        expected = [
            TextNode("The ", text_type_text),
            TextNode("word", text_type_bold),
            TextNode(" is important ", text_type_text),
            TextNode("because it is", text_type_bold),
            TextNode(".", text_type_text)
        ]
        self.assertListEqual(expected, split_nodes_delimiter([node], "**", text_type_bold))

    def test_delim_italic(self):
        node = TextNode("The *word* is important.", text_type_text)
        expected = [
            TextNode("The ", text_type_text),
            TextNode("word", text_type_italic),
            TextNode(" is important.", text_type_text),
        ]
        self.assertListEqual(expected, split_nodes_delimiter([node], "*", text_type_italic))

    def test_delim_multiple(self):
        node = TextNode(
            "The `TextNode` is a **type** that represents *text and its type*.",
            text_type_text
        )
        # First transform is for code
        first_transform = split_nodes_delimiter([node], "`", text_type_code)
        transform1_expected = [
            TextNode("The ", text_type_text),
            TextNode("TextNode", text_type_code),
            TextNode(" is a **type** that represents *text and its type*.", text_type_text),
        ]
        self.assertListEqual(transform1_expected, first_transform)
        # second transform is for bold
        second_transform = split_nodes_delimiter(first_transform, "**", text_type_bold)
        transform2_expected = [
            TextNode("The ", text_type_text),
            TextNode("TextNode", text_type_code),
            TextNode(" is a ", text_type_text),
            TextNode("type", text_type_bold),
            TextNode(" that represents *text and its type*.", text_type_text),
        ]
        self.assertListEqual(transform2_expected, second_transform)
        # final transform is for italic
        final_transform = split_nodes_delimiter(second_transform, "*", text_type_italic)
        final_expected = [
            TextNode("The ", text_type_text),
            TextNode("TextNode", text_type_code),
            TextNode(" is a ", text_type_text),
            TextNode("type", text_type_bold),
            TextNode(" that represents ", text_type_text),
            TextNode("text and its type", text_type_italic),
            TextNode(".", text_type_text),
        ]
        self.assertListEqual(final_expected, final_transform)

    def test_extract_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [
            ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
        ]
        actual = extract_markdown_images(text)
        self.assertListEqual(expected, actual)

    def test_extract_links(self):
        text = "If you can't exit VIM, try [google](https://www.google.com) or read the [documentation](https://neovim.io/doc/)"
        expected = [
            ("google", "https://www.google.com"),
            ("documentation", "https://neovim.io/doc/"),
        ]
        actual = extract_markdown_links(text)
        self.assertListEqual(expected, actual)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)",
            text_type_text,
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and ", text_type_text),
            TextNode("another", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png"),
        ]
        actual = split_nodes_image([node])
        self.assertListEqual(expected, actual)

    def test_split_images_image_first(self):
        node = TextNode(
            "![Thorn](https://upload.wikimedia.org/wikipedia/commons/8/8a/Latin_alphabet_%C3%9E%C3%BE.svg) was a letter in the English alphabet.",
            text_type_text
        )
        expected = [
            TextNode("Thorn", text_type_image, "https://upload.wikimedia.org/wikipedia/commons/8/8a/Latin_alphabet_%C3%9E%C3%BE.svg"),
            TextNode(" was a letter in the English alphabet.", text_type_text),
        ]
        actual = split_nodes_image([node])
        self.assertEqual(expected, actual)

    def test_split_links(self):
        node = TextNode(
            "If you can't exit VIM, try [google](https://www.google.com) or read the [documentation](https://neovim.io/doc/)",
            text_type_text,
        )
        expected = [
            TextNode("If you can't exit VIM, try ", text_type_text),
            TextNode("google", text_type_link, "https://www.google.com"),
            TextNode(" or read the ", text_type_text),
            TextNode("documentation", text_type_link, "https://neovim.io/doc/"),
        ]
        actual = split_nodes_link([node])
        self.assertListEqual(expected, actual)

    def test_split_link_link_first(self):
        node = TextNode(
                "[Neovim](https://neovim.io) is a great text editor for the tinkerer.",
            text_type_text,
        )
        expected = [
            TextNode("Neovim", text_type_link, "https://neovim.io"),
            TextNode(" is a great text editor for the tinkerer.", text_type_text),
        ]
        actual = split_nodes_link([node])
        self.assertListEqual(expected, actual)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        actual = text_to_textnodes(text)
        self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
