from __future__ import annotations

import re
from dataclasses import dataclass

import yaml
from docx.enum.text import WD_ALIGN_PARAGRAPH


# ── alignment map ─────────────────────────────────────────────────────────────

ALIGN_MAP: dict[str, WD_ALIGN_PARAGRAPH] = {
    "left":    WD_ALIGN_PARAGRAPH.LEFT,
    "center":  WD_ALIGN_PARAGRAPH.CENTER,
    "right":   WD_ALIGN_PARAGRAPH.RIGHT,
    "justify": WD_ALIGN_PARAGRAPH.JUSTIFY,
}

# ── regexes ───────────────────────────────────────────────────────────────────

PLACEHOLDER_RE = re.compile(r"^placeholder:(.+)$")
IMG_INLINE_RE  = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_DIV_OPEN_RE   = re.compile(r"^<div[^>]*\balign=[\"'](\w+)[\"'][^>]*>", re.I)
_DIV_CLOSE_RE  = re.compile(r"^</div>", re.I)
_ALIGN_PREFIX  = re.compile(r"^\{align:(\w+)\}\s*(.*)", re.I)
_PAGEBREAK_RE  = re.compile(r"^\{pagebreak\}\s*$", re.I)
_DIRECTIVE_RE  = re.compile(r"^:::(\S+)(?:\s+(.+?))?\s*$")
_DIRECTIVE_END = re.compile(r"^:::\s*$")


# ── content block ─────────────────────────────────────────────────────────────

@dataclass
class ContentBlock:
    text: str
    align: str = "left"
    is_pagebreak: bool = False
    directive: str = ""
    directive_title: str = ""


# ── preprocessor ──────────────────────────────────────────────────────────────

def preprocess_blocks(md_text: str) -> tuple[dict, list[ContentBlock]]:
    """Extract YAML frontmatter and split text into typed ContentBlocks."""
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
    dir_title = ""
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
                dir_name  = m.group(1).lower()
                dir_title = (m.group(2) or "").strip()
                in_directive = True
                dir_buf = []
                continue

        if in_directive:
            if _DIRECTIVE_END.match(line):
                blocks.append(ContentBlock(
                    "\n".join(dir_buf).strip(),
                    directive=dir_name,
                    directive_title=dir_title,
                ))
                in_directive = False
                dir_name  = ""
                dir_title = ""
                dir_buf   = []
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
