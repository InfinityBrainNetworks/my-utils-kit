# Sample Document

This document tests **doc-maker** — a custom Markdown to Word converter.
You can use *italic*, **bold**, ***bold italic***, and `inline code`.

## 1. Lists

### Unordered
- First item
- Second item
- Third item with `inline code`

### Ordered
1. Step one
2. Step two
3. Step three

## 2. Table

| Name  | Role      | Status   |
|-------|-----------|----------|
| Alice | Developer | Active   |
| Bob   | Designer  | Active   |
| Carol | Manager   | On Leave |

## 3. Code Block

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

print(greet("World"))
```

## 4. Blockquote

> This is an important note that should stand out visually in the final document.

---

## 5. Image Placeholders

![Company Logo](placeholder:company-logo)

{align:center} ![Header Banner](placeholder:header-banner)

## 6. Alignment

{align:center} This paragraph is centered using the inline align directive.

{align:right} This paragraph is right-aligned.

<div align="center">
This entire block is centered.
It can span multiple paragraphs inside the same div.
</div>

{pagebreak}

## 7. After Page Break

Content continues here after a manual page break.

This is the **final section** of the sample document.
