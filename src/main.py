from copy_static import copy_static, empty_web_content
from generate_page import generate_pages_recursive
import sys

def main():

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    empty_web_content("docs")
    copy_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()