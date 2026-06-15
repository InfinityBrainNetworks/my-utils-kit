# source_docs

Drop `.docx` files here that you want to reverse-engineer into a doc-maker template.

## How to use

1. Place your `.docx` file in this folder
2. Tell Claude: "inspect `source_docs/your-file.docx` and create a template named `your-style-name`"
3. Claude will analyse the styles, colours, and layout and generate:
   - `doc_maker/templates/your-style-name/theme.py`
   - `doc_maker/templates/your-style-name/renderer.py`
   - Registration in `doc_maker/templates/__init__.py`
4. Use it immediately: `doc-maker input.md --style your-style-name`

## Notes

- Files in this folder are gitignored (they may be large or proprietary)
- You can keep multiple source files here for different templates
