import os
import shutil
from markdown_blocks import markdown_to_blocks, markdown_to_html_node
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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        markdown = f.read()
    with open(template_path, 'r') as f:
        template = f.read()
    markdown_nodes = markdown_to_html_node(markdown)
    content = markdown_nodes.to_html()
    title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", content)
    directory_path = os.path.dirname(dest_path)
    os.makedirs(directory_path, exist_ok = True)
    with open(dest_path, 'w') as f:
        f.write(final_html)
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, file)
        if os.path.isfile(entry_path):
            if entry_path.endswith(".md"):
                generate_page(entry_path, template_path, os.path.join(dest_dir_path, file.replace(".md",".html")))
        elif os.path.isdir(entry_path):
            dest_path = os.path.join(dest_dir_path, file)
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            generate_pages_recursive(entry_path, template_path, dest_path)
        else:
            raise Exception("Invalid format for generation.")

def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)
    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)
    generate_pages_recursive("./content/", "./template.html", "./public")


main()
