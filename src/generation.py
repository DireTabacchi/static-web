import os
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Invalid page: no level 1 title/header")

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    src_fd = open(from_path)
    src_txt = src_fd.read()
    src_fd.close()

    template_fd = open(template_path)
    template_txt = template_fd.read()
    template_fd.close()

    html = markdown_to_html_node(src_txt).to_html()
    title = extract_title(src_txt)
    final_html = template_txt.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)
    dest_fd = open(dest_path, 'w')
    dest_fd.write(final_html)
    dest_fd.close()

def rec_generate_pages(dir_path_content, template_path, dest_dir_path):
    for content_path in os.listdir(dir_path_content):
        full_content_path = os.path.join(dir_path_content, content_path)
        if os.path.isfile(full_content_path):
            dest_file = f"{content_path.split(".")[0]}.html"
            dest = os.path.join(dest_dir_path, dest_file)
            generate_page(full_content_path, template_path, dest)
        else:
            rec_generate_pages(
                full_content_path,
                template_path,
                os.path.join(dest_dir_path, content_path)
            )
