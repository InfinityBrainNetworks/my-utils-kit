from __future__ import annotations

from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from ...core.base_renderer import BaseRenderer
from ...core.preprocessor import PLACEHOLDER_RE, IMG_INLINE_RE
from .theme import (
    PRIMARY, ACCENT, BODY, CAPTION,
    BORDER_SOFT, BORDER_H2,
    H2_PT, H3_PT, H4_PT, H5_PT,
    LABEL_DIRECTIVES,
)


class IbnCodexisRenderer(BaseRenderer):
    """
    Renders documents in the IBN Codexis Computer Science textbook style.

    Design language: flat typography, no coloured boxes.
    Structure is built through font size/weight/colour and paragraph borders.

    Heading levels:
      ##  H2 — major section (1.1 …)        16pt bold #2471A3, left+bottom border
      ### H3 — sub-section  (1.2.1 …)       12pt bold #2471A3, thin bottom border
      #### H4 — sub-sub-heading              10.5pt bold #1A5276, no border
      ##### H5 — inline label                10pt bold #1A5276, no border
    """

    # ── chapter opener ────────────────────────────────────────────────────────

    def render_chapter_opener(self, meta: dict) -> None:
        chapter_num = meta.get("chapter", "")
        title       = meta.get("title", "")
        subtitle    = meta.get("subtitle", "")

        # "CHAPTER N" small label
        if chapter_num:
            p = self.doc.add_paragraph()
            r = p.add_run(f"CHAPTER  {chapter_num}")
            r.font.size      = Pt(10)
            r.font.color.rgb = self._rgb(ACCENT)
            r.font.all_caps  = True
            r.font.bold      = True
            self._space_p(p, before=200, after=40)

        # Full-width coloured rule
        self._rule(ACCENT, sz="24")

        # Chapter title
        if title:
            p = self.doc.add_paragraph()
            r = p.add_run(title)
            r.bold           = True
            r.font.size      = Pt(22)
            r.font.color.rgb = self._rgb(PRIMARY)
            self._space_p(p, before=80, after=40)

        # Subtitle / description
        if subtitle:
            p = self.doc.add_paragraph()
            r = p.add_run(subtitle)
            r.italic         = True
            r.font.size      = Pt(11)
            r.font.color.rgb = self._rgb(CAPTION)
            self._space_p(p, before=0, after=160)

        self.doc.add_paragraph()

    # ── heading rendering (overrides base) ────────────────────────────────────

    def render_block(self, tok: dict) -> None:
        if tok["type"] == "heading":
            self._render_heading(tok)
        else:
            super().render_block(tok)

    def _render_heading(self, tok: dict) -> None:
        level = tok["level"]
        text  = self._text(tok.get("children", []))

        if level == 2:
            # Major section: left border (sz=24, #2471A3) + bottom border (sz=10, #1A5276)
            # 16pt bold, indented 120 dxa, spBefore=300, spAfter=120
            p = self.doc.add_paragraph()
            self._borders_p(p,
                left=   (ACCENT, "24"),
                bottom= (BORDER_H2, "10"),
            )
            self._indent_p(p, 120)
            self._space_p(p, before=300, after=120)
            r = p.add_run(text)
            r.bold           = True
            r.font.size      = Pt(H2_PT)
            r.font.color.rgb = self._rgb(ACCENT)

        elif level == 3:
            # Sub-section: thin bottom border (sz=4, #D6EEF8 pale blue)
            # 12pt bold, spBefore=220, spAfter=80
            p = self.doc.add_paragraph()
            self._borders_p(p, bottom=(BORDER_SOFT, "4"))
            self._space_p(p, before=220, after=80)
            r = p.add_run(text)
            r.bold           = True
            r.font.size      = Pt(H3_PT)
            r.font.color.rgb = self._rgb(ACCENT)

        elif level == 4:
            # Sub-sub-heading: no border, 10.5pt bold, spBefore=160, spAfter=60
            p = self.doc.add_paragraph()
            self._space_p(p, before=160, after=60)
            r = p.add_run(text)
            r.bold           = True
            r.font.size      = Pt(H4_PT)
            r.font.color.rgb = self._rgb(PRIMARY)

        elif level == 5:
            # Inline label: 10pt bold, spBefore=80, spAfter=40
            p = self.doc.add_paragraph()
            self._space_p(p, before=80, after=40)
            r = p.add_run(text)
            r.bold           = True
            r.font.size      = Pt(H5_PT)
            r.font.color.rgb = self._rgb(PRIMARY)

        else:
            # H6+ — plain bold body text
            p = self.doc.add_paragraph()
            r = p.add_run(text)
            r.bold = True
            r.font.color.rgb = self._rgb(BODY)

    # ── directive dispatcher ──────────────────────────────────────────────────

    def render_directive(self, name: str, text: str) -> None:
        if name == "figure":
            self._render_figure(text)
            return
        if name in ("table-note", "code-note"):
            self._render_caption(text)
            return

        cfg = LABEL_DIRECTIVES.get(name)
        if cfg:
            label, color, pt = cfg
            self._label_block(label, color, pt, text)
        else:
            tokens = self._md(text)
            if tokens:
                self.render_tokens(tokens)

    # ── flat label block (no coloured box) ───────────────────────────────────

    def _label_block(self, label: str, color: str, pt: float, text: str) -> None:
        """Renders a bold label line followed by body-styled content."""
        # Label paragraph
        p = self.doc.add_paragraph()
        r = p.add_run(label)
        r.bold           = True
        r.font.size      = Pt(pt)
        r.font.color.rgb = self._rgb(color)
        self._space_p(p, before=160, after=80)

        # Content
        for tok in (self._md(text) or []):
            self.render_block(tok)

        self.doc.add_paragraph()

    # ── figure: image placeholder + bold-italic caption ──────────────────────

    def _render_figure(self, text: str) -> None:
        lines = [ln for ln in text.strip().splitlines() if ln.strip()]
        img_match = None
        caption_parts: list[str] = []

        for line in lines:
            m = IMG_INLINE_RE.search(line.strip())
            if m and img_match is None:
                img_match = m
            else:
                caption_parts.append(line.strip())

        # Image / placeholder
        p_img = self.doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if img_match:
            alt, src = img_match.group(1), img_match.group(2)
            ph = PLACEHOLDER_RE.match(src)
            if ph:
                self._image_placeholder(p_img, ph.group(1), alt)
            else:
                r = p_img.add_run(f"[ IMAGE: {alt or src} ]")
                r.font.italic    = True
                r.font.color.rgb = self._rgb(CAPTION)
        self._space_p(p_img, before=60, after=40)

        # Caption: bold italic, #1A5276, ~9pt
        if caption_parts:
            p_cap = self.doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p_cap.add_run(" ".join(caption_parts))
            r.bold           = True
            r.italic         = True
            r.font.size      = Pt(9)
            r.font.color.rgb = self._rgb(PRIMARY)
            self._space_p(p_cap, before=0, after=160)

        self.doc.add_paragraph()

    # ── table / code / pseudo-code caption ───────────────────────────────────

    def _render_caption(self, text: str) -> None:
        """Small italic grey caption line (for Table X.X, Code X.X, Pseudo Code X.X)."""
        p = self.doc.add_paragraph()
        r = p.add_run(text.strip())
        r.italic         = True
        r.font.size      = Pt(8.5)
        r.font.color.rgb = self._rgb(CAPTION)
        self._space_p(p, before=40, after=160)
