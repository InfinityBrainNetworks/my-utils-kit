# doc-maker

Convert custom Markdown to Word (`.docx`) documents. Fully local, no internet required.

## Install

```bash
cd packages/doc-maker
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
# Convert a .md file to .docx
doc-maker samples/sample.md

# Specify output path
doc-maker samples/sample.md --output output/report.docx

# Use a custom .docx template
doc-maker samples/sample.md --template templates/corporate.docx --output output/report.docx
```

Or run as a module:

```bash
python -m doc_maker.cli samples/sample.md
```

## Custom Syntax

On top of standard Markdown, doc-maker supports:

| Syntax | Description |
| ------ | ----------- |
| `{pagebreak}` | Insert a page break |
| `{align:center} text` | Single-line alignment (`left`, `center`, `right`, `justify`) |
| `<div align="center">...</div>` | Multi-paragraph alignment block |
| `![alt](placeholder:name)` | Image placeholder slot |

## Supported Elements

- Headings (H1–H6)
- Bold, italic, bold-italic, inline code, strikethrough
- Unordered and ordered lists (with nesting)
- Tables
- Code blocks (with language label)
- Blockquotes
- Horizontal rules

## Project Structure

```text
doc-maker/
├── doc_maker/
│   ├── __init__.py
│   ├── builder.py   # core parser + docx renderer
│   └── cli.py       # CLI entry point
├── samples/
│   └── sample.md    # test document covering all features
├── output/          # generated files (gitignored)
└── requirements.txt
```
