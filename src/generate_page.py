from md_to_html import markdown_to_html_node
import os

def extract_title(markdown: str):
    for line in markdown.split('\n'):
        if line.startswith('# '):
            return line[2:].strip()
    else:
        raise ValueError("title not found")

def generate_page(from_path, template_path, dest_path):
    print(f'Generating a page from {from_path} to {dest_path} using {template_path}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(from_path) as markdown, open(template_path) as template, open(dest_path, "w") as new_page:
        md_text = markdown.read()
        template_text = template.read()

        md_to_html = markdown_to_html_node(md_text).to_html()
        md_title = extract_title(md_text)

        new_template = template_text.replace("{{ Title }}", md_title)
        new_template = new_template.replace("{{ Content }}", md_to_html)

        new_page.write(new_template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):

        item_path = os.path.join(dir_path_content, item)
        target_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(item_path):
            if not item.endswith(".md"):
                continue
            target_html = target_path[:-3] + ".html"
            generate_page(item_path, template_path, target_html)
        else:
            generate_pages_recursive(item_path, template_path, target_path)