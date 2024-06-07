import os
import shutil

from copystatic import rec_copy_files
import generation


static_dir = "./static"
public_dir = "./public"
content_dir = "./content"
template = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    print("Copying static files to public directory...")
    rec_copy_files(static_dir, public_dir)

    print("Generating page...")
    generation.generate_page(
        os.path.join(content_dir, "index.md"),
        template,
        os.path.join(public_dir, "index.html")
    )


main()
