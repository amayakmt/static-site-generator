from copy_static import empty_public, copy_static
from generate_page import generate_pages_recursive

def main():
    empty_public()
    copy_static("static", "public")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()