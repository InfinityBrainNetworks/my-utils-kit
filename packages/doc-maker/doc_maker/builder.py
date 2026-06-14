from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import mistune
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ── alignment ─────────────────────────────────────────────────────────────────

ALIGN_MAP: dict[str, WD_ALIGN_PARAGRAPH] = {
    "left":    WD_ALIGN_PARAGRAPH.LEFT,
    "center":  WD_ALIGN_PARAGRAPH.CENTER,
    "right":   WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

_PLACEHOLDER_RE = re.compile(r"^placeholder:(.+)$")
_DIV_OPEN_RE    = re.compile(r"^<div[^>]*\balign=[\"'](\w+)[\"'][^>]*>", re.I)
_DIV_CLOSE_RE   = re.compile(r"^</div>", re.I)
_ALIGN_PREFIX   = re.compile(r"^\{align:(\w+)\}\s*(.*)", re.I)
_PAGEBREAK_RE   = re.compile(r"^\{pagebreak\}\s*$", re.I)


# ── preprocessing ─────────────────────────────────────────────────────────────

@dataclass
class ContentBlock:
    text: str
    align: str = "left"
    is_pagebreak: bool = False


def preprocess_blocks(md_text: str) -> list[ContentBlock]:
    """Split markdown into content blocks, each carrying an alignment."""
    blocks: list[ContentBlock] = []
    current_align = "left"
    buffer: list[str] = []

    def flush():
        nonlocal buffer
        if buffer:
            blocks.append(ContentBlock("\n".join(buffer), align=current_align))
            buffer = []

    for line in md_text.splitlines():
        if _PAGEBREAK_RE.match(line):
            flush()
            blocks.append(ContentBlock("", is_pagebreak=True))
            continue

        m = _DIV_OPEN_RE.match(line)
        if m:
            flush()
            current_align = m.group(1).lower()
            continue

        if _DIV_CLOSE_RE.match(line):
            flush()
            current_align = "left"
            continue

        m = _ALIGN_PREFIX.match(line)
        if m:
            flush()
            blocks.append(ContentBlock(m.group(2), align=m.group(1).lower()))
            continue

        buffer.append(line)

    flush()
    return blocks


# ── builder ───────────────────────────────────────────────────────────────────

class DocxBuilder:
    def __init__(self, template_path: Optional[Path] = None):
        self.doc = Document(str(template_path)) if template_path else Document()
        self._align = WD_ALIGN_PARAGRAPH.LEFT
        # renderer='ast' returns a list of token dicts instead of HTML
        self._md = mistune.create_markdown(renderer="ast", plugins=["table", "strikethrough"])

    def build(self, md_text: str) -> Document:
        for block in preprocess_blocks(md_text):
            if block.is_pagebreak:
                self._page_break()
                continue
            self._align = ALIGN_MAP.get(block.align, WD_ALIGN_PARAGRAPH.LEFT)
            tokens = self._md(block.text)
            if tokens:
                self._render_tokens(tokens)
        return self.doc

    # ── block rendering ───────────────────────────────────────────────────────

    def _render_tokens(self, tokens: list):
        for tok in tokens:
            self._render_block(tok)

    def _render_block(self, tok: dict):
        t = tok["type"]

        if t == "heading":
            self.doc.add_heading(self._text(tok.get("children", [])), level=tok["level"])

        elif t in ("paragraph", "block_text"):
            p = self.doc.add_paragraph()
            p.alignment = self._align
            self._inline(p, tok.get("children", []))

        elif t in ("newline", "blank_line"):
            pass

        elif t == "thematic_break":
            self._hr()

        elif t == "block_code":
            self._code_block(tok.get("text", ""), tok.get("info", "") or "")

        elif t == "block_quote":
            for child in tok.get("children", []):
                if child["type"] == "paragraph":
                    p = self.doc.add_paragraph(style="Intense Quote")
                    self._inline(p, child.get("children", []))

        elif t == "list":
            self._list(tok.get("children", []), tok.get("ordered", False))

        elif t == "table":
            self._table(tok)

    # ── list ──────────────────────────────────────────────────────────────────

    def _list(self, items: list, ordered: bool):
        style = "List Number" if ordered else "List Bullet"
        for item in items:
            if item["type"] != "list_item":
                continue
            inline_children: list = []
            sub_lists: list = []
            for child in item.get("children", []):
                if child["type"] == "list":
                    sub_lists.append(child)
                elif child["type"] in ("paragraph", "block_text"):
                    inline_children.extend(child.get("children", []))
                else:
                    inline_children.append(child)
            p = self.doc.add_paragraph(style=style)
            p.alignment = self._align
            self._inline(p, inline_children)
            for sub in sub_lists:
                self._list(sub.get("children", []), sub.get("ordered", False))

    # ── table ─────────────────────────────────────────────────────────────────

    def _table(self, tok: dict):
        head = next((c for c in tok.get("children", []) if c["type"] == "table_head"), None)
        body = next((c for c in tok.get("children", []) if c["type"] == "table_body"), None)

        # table_head: direct table_cell children (no row wrapper)
        head_cells = head.get("children", []) if head else []
        # table_body: table_row → table_cell
        body_rows  = body.get("children", []) if body else []

        cols       = max(len(head_cells), max((len(r.get("children", [])) for r in body_rows), default=0))
        total_rows = 1 + len(body_rows) if head_cells else len(body_rows)
        if cols == 0 or total_rows == 0:
            return

        table = self.doc.add_table(rows=total_rows, cols=cols)
        table.style = "Table Grid"

        # Header row
        r_idx = 0
        if head_cells:
            for c_idx, cell_tok in enumerate(head_cells):
                cell = table.cell(0, c_idx)
                cell.text = ""
                p = cell.paragraphs[0]
                self._inline(p, cell_tok.get("children", []))
                for run in p.runs:
                    run.bold = True
            r_idx = 1

        # Body rows
        for row in body_rows:
            for c_idx, cell_tok in enumerate(row.get("children", [])):
                cell = table.cell(r_idx, c_idx)
                cell.text = ""
                p = cell.paragraphs[0]
                self._inline(p, cell_tok.get("children", []))
            r_idx += 1

    # ── inline rendering ──────────────────────────────────────────────────────

    def _inline(self, p, tokens: list, bold: bool = False, italic: bool = False):
        for tok in tokens:
            self._inline_tok(p, tok, bold, italic)

    def _inline_tok(self, p, tok: dict, bold: bool, italic: bool):
        t = tok["type"]

        if t == "text":
            r = p.add_run(tok.get("text", ""))
            r.bold   = bold
            r.italic = italic

        elif t == "strong":
            self._inline(p, tok.get("children", []), bold=True, italic=italic)

        elif t == "emphasis":
            self._inline(p, tok.get("children", []), bold=bold, italic=True)

        elif t == "codespan":
            r = p.add_run(tok.get("text", ""))
            r.bold           = bold
            r.italic         = italic
            r.font.name      = "Courier New"
            r.font.size      = Pt(10)
            r.font.color.rgb = RGBColor(0xC7, 0x25, 0x4E)

        elif t == "strikethrough":
            for child in tok.get("children", []):
                r = p.add_run(self._text([child]))
                r.font.strike = True

        elif t == "image":
            src = tok.get("src", "")
            alt = tok.get("alt", "") or ""
            m   = _PLACEHOLDER_RE.match(src)
            if m:
                self._image_placeholder(p, m.group(1), alt)

        elif t == "link":
            r = p.add_run(self._text(tok.get("children", [])))
            r.bold           = bold
            r.italic         = italic
            r.font.color.rgb = RGBColor(0x00, 0x56, 0xB3)
            r.underline      = True

        elif t == "softlinebreak":
            p.add_run(" ")

        elif t == "linebreak":
            p.add_run("\n")

    # ── helpers ───────────────────────────────────────────────────────────────

    def _text(self, tokens: list) -> str:
        parts = []
        for tok in tokens:
            if tok["type"] in ("text", "codespan"):
                parts.append(tok.get("text", ""))
            elif "children" in tok:
                parts.append(self._text(tok["children"]))
        return "".join(parts)

    def _page_break(self):
        p   = self.doc.add_paragraph()
        run = p.add_run()
        br  = OxmlElement("w:br")
        br.set(qn("w:type"), "page")
        run._r.append(br)

    def _hr(self):
        p   = self.doc.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        bdr = OxmlElement("w:pBdr")
        bot = OxmlElement("w:bottom")
        bot.set(qn("w:val"),   "single")
        bot.set(qn("w:sz"),    "6")
        bot.set(qn("w:space"), "1")
        bot.set(qn("w:color"), "AAAAAA")
        bdr.append(bot)
        pPr.append(bdr)

    def _code_block(self, code: str, lang: str = ""):
        p   = self.doc.add_paragraph(style="No Spacing")
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  "F5F5F5")
        pPr.append(shd)
        r = p.add_run(code)
        r.font.name = "Courier New"
        r.font.size = Pt(9)

    def _image_placeholder(self, p, name: str, alt: str = ""):
        label = alt or name
        r = p.add_run(f"[ IMAGE: {label} ]")
        r.font.name      = "Arial"
        r.font.size      = Pt(10)
        r.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
        r.font.italic    = True
