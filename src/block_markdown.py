from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)

    return filtered_blocks


def block_to_block_type(block_text):
    block_lines = block_text.split("\n")
    if (
        block_text.startswith("# ")
        or block_text.startswith("## ")
        or block_text.startswith("### ")
        or block_text.startswith("#### ")
        or block_text.startswith("##### ")
        or block_text.startswith("###### ")
    ):
        return block_type_heading
    if (
        len(block_lines) > 0
		and block_lines[0].startswith("```")
		and block_lines[-1].startswith("```")
    ):
        return block_type_code
    if block_text.startswith(">"):
        for line in block_lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block_text.startswith("* "):
        for line in block_lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block_text.startswith("- "):
        for line in block_lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block_text.startswith("1. "):
        oi = 1
        for line in block_lines:
            if not line.startswith(f"{oi}. "):
                return block_type_paragraph
            oi += 1
        return block_type_olist
    return block_type_paragraph


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(markdown_block):
    block_type = block_to_block_type(markdown_block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(markdown_block)
    if block_type == block_type_heading:
        return heading_to_html_node(markdown_block)
    if block_type == block_type_code:
        return code_to_html_node(markdown_block)
    if block_type == block_type_quote:
        return quote_to_html_node(markdown_block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(markdown_block)
    if block_type == block_type_olist:
        return olist_to_html_node(markdown_block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        children.append(html_node)
    return children


def paragraph_to_html_node(markdown_block):
    lines = markdown_block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(markdown_block):
    level = 0
    for char in markdown_block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(markdown_block):
        raise ValueError(f"Invalid heading at level: {level}")
    text = markdown_block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(markdown_block):
    if not markdown_block.startswith("```") or not markdown_block.endswith("```"):
        raise ValueError("Invalid code block")
    text = markdown_block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_to_html_node(markdown_block):
    block_lines = markdown_block.split("\n")
    new_lines = []
    for block_line in block_lines:
        if not block_line.startswith("> "):
            raise ValueError("Invalid quote block")
        new_lines.append(block_line.lstrip("> "))
    quote = " ".join(new_lines)
    children = text_to_children(quote)
    return ParentNode("blockquote", children)

def ulist_to_html_node(markdown_block):
    items = markdown_block.split("\n")
    ul_children = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        ul_children.append(ParentNode("li", children))
    return ParentNode("ul", ul_children)

def olist_to_html_node(markdown_block):
    items = markdown_block.split("\n")
    ol_children = []
    oi = 1
    for item in items:
        prefix_len = len(f"{oi}. ")
        text = item[prefix_len:]
        children = text_to_children(text)
        ol_children.append(ParentNode("li", children))
        oi += 1
    return ParentNode("ol", ol_children)
