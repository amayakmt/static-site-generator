# Static Site Generator

A small static site generator written in pure Python — no external dependencies. Reads a tree of Markdown files, applies an HTML template, and produces a deployable static site.

**Live demo:** https://amayakmt.github.io/static-site-generator

## Features

- Markdown → HTML conversion supporting:
  - Headings (`#` through `######`)
  - Paragraphs
  - Fenced code blocks (`` ``` ``)
  - Block quotes (`>`)
  - Unordered (`-`) and ordered (`1.`) lists
  - Inline formatting: `**bold**`, `_italic_`, `` `code` ``, `[links](url)`, `![images](url)`
- Recursive directory traversal — mirrors your `content/` tree into the output
- Configurable base path (so the same code works on `localhost` and on a GitHub Pages subpath)
- Static asset copy (CSS, images) from `static/` into the output
- Unit-tested

## Project layout

```
.
├── content/          Markdown source files (mirrored into output)
├── static/           Static assets (CSS, images) copied as-is
├── template.html     HTML wrapper with {{ Title }} and {{ Content }} placeholders
├── src/              Python source
│   ├── main.py
│   ├── copy_static.py
│   ├── generate_page.py
│   ├── md_to_html.py
│   ├── split_blocks.py
│   ├── convert_raw.py
│   ├── textnode.py
│   ├── htmlnode.py
│   ├── extract_md_objects.py
│   └── test_*.py
├── docs/             Build output (served by GitHub Pages)
├── build.sh          Production build
├── main.sh           Local dev build + server
└── test.sh           Run all unit tests
```

## Quick start

Requires Python 3.10+ (uses `match`/`case`).

### Local development

```bash
./main.sh
```

This builds the site with base path `/` and serves it on `http://localhost:8888/`.

### Production build

```bash
./build.sh
```

Builds with the GitHub Pages base path (`/static-site-generator/`). Output goes to `docs/`, which is the directory GitHub Pages serves from on the `main` branch.

### Tests

```bash
./test.sh
```

Runs all `test_*.py` modules via `unittest`.

## How it works

The pipeline is a chain of small, testable transformations:

1. **`markdown_to_blocks`** — splits the document on blank lines into independent blocks.
2. **`block_to_block_type`** — classifies each block (paragraph, heading, list, etc.).
3. **`text_to_textnodes`** — parses inline markdown within a block into a flat list of `TextNode`s (one per delimited run).
4. **`text_node_to_html_node`** — converts each `TextNode` into a `LeafNode` with the appropriate HTML tag.
5. **`markdown_to_html_node`** — assembles block-level `ParentNode`s containing the inline children, wraps the lot in a single `<div>`, and returns the root.
6. **`generate_page`** — renders that root via `to_html()`, splices it into the template, rewrites root-relative URLs to honor the base path, and writes the resulting HTML to disk.
7. **`generate_pages_recursive`** — walks `content/`, calling `generate_page` for every `.md` file and recreating the directory structure in `docs/`.

The HTML node model is two classes: `LeafNode` (terminal, has a value) and `ParentNode` (has a list of children), both descended from `HTMLNode`. Rendering is a simple recursive concatenation.

## Deployment

The `docs/` directory is committed and served directly by GitHub Pages from the `main` branch. To deploy:

```bash
./build.sh
git add docs
git commit -m "rebuild site"
git push
```

GitHub Pages picks up the change automatically.

## License

MIT