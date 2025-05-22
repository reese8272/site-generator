import os
import shutil
from markdown_blocks import markdown_to_blocks
from copystatic import copy_files_recursive


dir_path_static = "./static"
dir_path_public = "./public"


def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    block = blocks[0]
    if block.startswith("#") and block[1:2] != "#":
        title = block[1:].strip()
        return title
    else:
        raise Exception("No Heading Found")

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)


main()
