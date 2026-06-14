from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import yaml
import mistune
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ── constants ─────────────────────────────────────────────────────────────────

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
_DIRECTIVE_RE   = re.compile(r"^:::(\S+)\s*$")
_DIRECTIVE_END  = re.compile(r"^:::\s*$")
_IMG_INLINE_RE  = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

# ── directive config: (label, header_fill, content_fill) ─────────────────────
# Each entry drives the generic box renderer — add new directives here only.

_DIRECTIVE_CONFIG: dict[str, tuple[str, str, str]] = {
    # Phase 1 — page structure
    "learning-objectives":   ("LEARNING OBJECTIVES",   "1B5E8C", "D6E4F0"),
    "getting-started":       ("GETTING STARTED",        "1F6B42", "D9EFE3"),
    # Phase 2 — callout / info boxes
    "key-term":              ("KEY TERM",               "6A1B9A", "F3E5F5"),
    "key-terms":             ("KEY TERMS",              "6A1B9A", "F3E5F5"),
    "subject-vocabulary":    ("SUBJECT VOCABULARY",     "00695C", "E0F2F1"),
    "tip":                   ("TIP",                    "BF360C", "FBE9E7"),
    "exam-tip":              ("EXAM TIP",               "B71C1C", "FFEBEE"),
    "did-you-know":          ("DID YOU KNOW?",          "01579B", "E1F5FE"),
    "hint":                  ("HINT",                   "E65100", "FFF8E1"),
    "extend-your-knowledge": ("EXTEND YOUR KNOWLEDGE",  "283593", "E8EAF6"),
    "maths-skills":          ("MATHS SKILLS",           "1565C0", "E3F2FD"),
    "skills-link":           ("SKILLS LINK",            "37474F", "ECEFF1"),
    "international-context": ("INTERNATIONAL CONTEXT",  "1B5E20", "E8F5E9"),
    # Phase 3 — worked content
    "worked-example":         ("WORKED EXAMPLE",          "004D40", "E0F2F1"),
    "worked-solution":        ("WORKED SOLUTION",          "006064", "E0F7FA"),
    # Phase 3 — exercise / assessment
    "activity":               ("ACTIVITY",                 "E65100", "FFF3E0"),
    "exercise":               ("EXERCISE",                 "1A237E", "E8EAF6"),
    "checkpoint":             ("CHECKPOINT",               "4A148C", "F3E5F5"),
    "strengthen":             ("STRENGTHEN",               "1B5E20", "E8F5E9"),
    "challenge":              ("CHALLENGE",                "0D47A1", "E3F2FD"),
    "exam-style-questions":   ("EXAM-STYLE QUESTIONS",     "B71C1C", "FFEBEE"),
    "unit-questions":         ("UNIT QUESTIONS",           "4A148C", "EDE7F6"),
    # Phase 3 — end of chapter
    "chapter-summary":        ("CHAPTER SUMMARY",          "37474F", "ECEFF1"),
    "key-points":             ("KEY POINTS",               "1B5E20", "E8F5E9"),
    # Phase 3 — margin note
    "margin-note":            ("MARGIN NOTE",              "F57F17", "FFF9C4"),
}


# ── preprocessing ─────────────────────────────────────────────────────────────

@dataclass
class ContentBlock:
    text: str
    align: str = "left"
    is_pagebreak: bool = False
    directive: str = ""


def preprocess_blocks(md_text: str) -> tuple[dict, list[ContentBlock]]:
    """Extract YAML frontmatter and split text into typed content blocks."""
    meta: dict = {}
    content = md_text.strip()

    fm = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    if fm:
        try:
            meta = yaml.safe_load(fm.group(1)) or {}
        except yaml.YAMLError:
            pass
        content = content[fm.end():].strip()

    blocks: list[ContentBlock] = []
    buffer: list[str] = []
    current_align = "left"
    in_directive = False
    dir_name = ""
    dir_buf: list[str] = []

    def flush():
        nonlocal buffer
        joined = "\n".join(buffer).strip()
        if joined:
            blocks.append(ContentBlock(joined, align=current_align))
        buffer = []

    for line in content.splitlines():
        if not in_directive:
            m = _DIRECTIVE_RE.match(line)
            if m:
                flush()
                dir_name = m.group(1).lower()
                in_directive = True
                dir_buf = []
                continue

        if in_directive:
            if _DIRECTIVE_END.match(line):
                blocks.append(ContentBlock(
                    "\n".join(dir_buf).strip(),
                    directive=dir_name,
                ))
                in_directive = False
                dir_name = ""
                dir_buf = []
            else:
                dir_buf.append(line)
            continue

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
    return meta, blocks


# ── builder ───────────────────────────────────────────────────────────────────

class DocxBuilder:
    def __init__(self, template_path: Optional[Path] = None):
        self.doc = Document(str(template_path)) if template_path else Document()
        self._align = WD_ALIGN_PARAGRAPH.LEFT
        self._md = mistune.create_markdown(
            renderer="ast", plugins=["table", "strikethrough"]
        )

    def build(self, md_text: str) -> Document:
        meta, blocks = preprocess_blocks(md_text)

        if meta:
            self._chapter_opener(meta)

        for block in blocks:
            if block.is_pagebreak:
                self._page_break()
            elif block.directive:
                self._render_directive(block.directive, block.text)
            else:
                self._align = ALIGN_MAP.get(block.align, WD_ALIGN_PARAGRAPH.LEFT)
                tokens = self._md(block.text)
                if tokens:
                    self._render_tokens(tokens)

        return self.doc

    # ── chapter opener ────────────────────────────────────────────────────────

    def _chapter_opener(self, meta: dict):
        chapter_num = meta.get("chapter", "")
        title       = meta.get("title", "")
        subtitle    = meta.get("subtitle", "")
        cover_image = meta.get("cover_image", "")

        # Cover image placeholder — full width feel
        if cover_image:
            m = _PLACEHOLDER_RE.match(str(cover_image))
            if m:
                p = self.doc.add_paragraph()
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                self._shade_p(p, "E8EDF2")
                r = p.add_run(f"\n  [ IMAGE: {m.group(1)} ]\n")
                r.font.name      = "Arial"
                r.font.size      = Pt(10)
                r.font.color.rgb = self._rgb("1B5E8C")
                r.font.italic    = True

        # "CHAPTER N" label
        if chapter_num:
            p = self.doc.add_paragraph()
            r = p.add_run(f"CHAPTER  {chapter_num}")
            r.font.size      = Pt(10)
            r.font.color.rgb = self._rgb("1B5E8C")
            r.font.all_caps  = True
            r.font.bold      = True

        # Coloured rule
        self._rule("1B5E8C", sz="18")

        # Chapter title
        if title:
            p = self.doc.add_paragraph()
            r = p.add_run(title)
            r.bold           = True
            r.font.size      = Pt(26)
            r.font.color.rgb = self._rgb("1B5E8C")

        # Subtitle
        if subtitle:
            p = self.doc.add_paragraph()
            r = p.add_run(subtitle)
            r.italic         = True
            r.font.size      = Pt(12)
            r.font.color.rgb = self._rgb("555555")

        self.doc.add_paragraph()  # breathing room

    # ── directive dispatcher ──────────────────────────────────────────────────

    def _render_directive(self, name: str, text: str):
        if name == "figure":
            self._render_figure(text)
            return
        if name == "diagram-placeholder":
            self._render_diagram_placeholder(text)
            return
        cfg = _DIRECTIVE_CONFIG.get(name)
        if cfg:
            label, header_fill, content_fill = cfg
            self._generic_box(label, header_fill, content_fill, text)
        else:
            tokens = self._md(text)
            if tokens:
                self._render_tokens(tokens)

    def _generic_box(self, label: str, header_fill: str, content_fill: str, text: str):
        self._box_header(label, header_fill, "FFFFFF")
        for tok in (self._md(text) or []):
            self._block_in_box(tok, fill=content_fill, border=header_fill)
        self.doc.add_paragraph()

    def _render_figure(self, text: str):
        lines = [ln for ln in text.strip().splitlines() if ln.strip()]
        img_match = None
        caption_parts: list[str] = []

        for line in lines:
            m = _IMG_INLINE_RE.search(line.strip())
            if m and img_match is None:
                img_match = m
            else:
                caption_parts.append(line.strip())

        p_img = self.doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if img_match:
            alt, src = img_match.group(1), img_match.group(2)
            ph = _PLACEHOLDER_RE.match(src)
            if ph:
                self._image_placeholder(p_img, ph.group(1), alt)
            else:
                r = p_img.add_run(f"[ IMAGE: {alt or src} ]")
                r.font.italic    = True
                r.font.color.rgb = self._rgb("888888")

        if caption_parts:
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p_cap.add_run(" ".join(caption_parts))
            r.italic         = True
            r.font.size      = Pt(9)
            r.font.color.rgb = self._rgb("444444")

        self.doc.add_paragraph()

    def _render_diagram_placeholder(self, text: str):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        self._shade_p(p, "EEEEEE")
        r = p.add_run(f"\n  [ DIAGRAM: {text.strip()} ]\n")
        r.font.name      = "Arial"
        r.font.size      = Pt(10)
        r.font.color.rgb = self._rgb("666666")
        r.italic         = True
        self.doc.add_paragraph()

    # ── box primitives ────────────────────────────────────────────────────────

    def _box_header(self, label: str, fill: str, text_color: str):
        p = self.doc.add_paragraph()
        self._shade_p(p, fill)
        r = p.add_run(f"  {label}")
        r.bold           = True
        r.font.size      = Pt(10)
        r.font.color.rgb = self._rgb(text_color)
        r.font.all_caps  = True

    def _block_in_box(self, tok: dict, fill: str, border: str):
        t = tok["type"]
        if t in ("paragraph", "block_text"):
            p = self.doc.add_paragraph()
            self._shade_p(p, fill)
            self._left_border(p, border)
            self._indent_p(p, 280)
            self._inline(p, tok.get("children", []))

        elif t == "list":
            ordered = tok.get("ordered", False)
            style   = "List Number" if ordered else "List Bullet"
            for item in tok.get("children", []):
                if item["type"] != "list_item":
                    continue
                inline: list = []
                for child in item.get("children", []):
                    if child["type"] in ("paragraph", "block_text"):
                        inline.extend(child.get("children", []))
                    else:
                        inline.append(child)
                p = self.doc.add_paragraph(style=style)
                self._shade_p(p, fill)
                self._left_border(p, border)
                self._inline(p, inline)

        elif t not in ("newline", "blank_line"):
            self._render_block(tok)

    # ── block rendering ───────────────────────────────────────────────────────

    def _render_tokens(self, tokens: list):
        for tok in tokens:
            self._render_block(tok)

    def _render_block(self, tok: dict):
        t = tok["type"]

        if t == "heading":
            self.doc.add_heading(
                self._text(tok.get("children", [])), level=tok["level"]
            )

        elif t in ("paragraph", "block_text"):
            p = self.doc.add_paragraph()
            p.alignment = self._align
            self._inline(p, tok.get("children", []))

        elif t in ("newline", "blank_line"):
            pass

        elif t == "thematic_break":
            self._rule()

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
        head_cells = head.get("children", []) if head else []
        body_rows  = body.get("children", []) if body else []
        all_rows   = ([{"children": head_cells}] if head_cells else []) + body_rows
        if not all_rows:
            return
        cols  = max(len(r.get("children", [])) for r in all_rows)
        table = self.doc.add_table(rows=len(all_rows), cols=cols)
        table.style = "Table Grid"
        for r_idx, row in enumerate(all_rows):
            is_head = r_idx == 0 and bool(head_cells)
            for c_idx, cell_tok in enumerate(row.get("children", [])):
                cell = table.cell(r_idx, c_idx)
                cell.text = ""
                p = cell.paragraphs[0]
                self._inline(p, cell_tok.get("children", []))
                if is_head:
                    for run in p.runs:
                        run.bold = True

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

    # ── XML / style helpers ───────────────────────────────────────────────────

    def _text(self, tokens: list) -> str:
        parts = []
        for tok in tokens:
            if tok["type"] in ("text", "codespan"):
                parts.append(tok.get("text", ""))
            elif "children" in tok:
                parts.append(self._text(tok["children"]))
        return "".join(parts)

    def _rgb(self, hex_str: str) -> RGBColor:
        h = hex_str.lstrip("#")
        return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

    def _shade_p(self, p, fill: str):
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"),   "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"),  fill.upper())
        pPr.append(shd)

    def _left_border(self, p, color: str, sz: str = "18"):
        pPr = p._p.get_or_add_pPr()
        bdr  = OxmlElement("w:pBdr")
        left = OxmlElement("w:left")
        left.set(qn("w:val"),   "single")
        left.set(qn("w:sz"),    sz)
        left.set(qn("w:space"), "4")
        left.set(qn("w:color"), color.upper())
        bdr.append(left)
        pPr.append(bdr)

    def _indent_p(self, p, left: int = 360):
        pPr = p._p.get_or_add_pPr()
        ind = OxmlElement("w:ind")
        ind.set(qn("w:left"), str(left))
        pPr.append(ind)

    def _rule(self, color: str = "AAAAAA", sz: str = "6"):
        p   = self.doc.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        bdr = OxmlElement("w:pBdr")
        bot = OxmlElement("w:bottom")
        bot.set(qn("w:val"),   "single")
        bot.set(qn("w:sz"),    sz)
        bot.set(qn("w:space"), "1")
        bot.set(qn("w:color"), color.upper())
        bdr.append(bot)
        pPr.append(bdr)

    def _page_break(self):
        p   = self.doc.add_paragraph()
        run = p.add_run()
        br  = OxmlElement("w:br")
        br.set(qn("w:type"), "page")
        run._r.append(br)

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
