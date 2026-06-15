from __future__ import annotations

from pathlib import Path
from typing import Optional

import mistune
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH

from .core.preprocessor import preprocess_blocks, ALIGN_MAP
from .templates import REGISTRY, DEFAULT_STYLE


class DocxBuilder:
    """
    Orchestrates document generation.

    Accepts a style name (e.g. "pearson-edexcel") and delegates all
    rendering to the registered template renderer for that style.
    Adding a new template requires no changes here.
    """

    def __init__(
        self,
        style: str = DEFAULT_STYLE,
        base_doc: Optional[Path] = None,
    ):
        renderer_cls = REGISTRY.get(style)
        if renderer_cls is None:
            available = ", ".join(REGISTRY)
            raise ValueError(f"Unknown style '{style}'. Available: {available}")

        self.doc = Document(str(base_doc)) if base_doc else Document()
        self._md = mistune.create_markdown(
            renderer="ast", plugins=["table", "strikethrough"]
        )
        self._renderer = renderer_cls(self.doc, self._md)

    def build(self, md_text: str) -> Document:
        meta, blocks = preprocess_blocks(md_text)

        if meta:
            self._renderer.render_chapter_opener(meta)

        for block in blocks:
            if block.is_pagebreak:
                self._renderer._page_break()
            elif block.directive:
                self._renderer.render_directive(block.directive, block.text)
            else:
                self._renderer._align = ALIGN_MAP.get(
                    block.align, WD_ALIGN_PARAGRAPH.LEFT
                )
                tokens = self._md(block.text)
                if tokens:
                    self._renderer.render_tokens(tokens)

        return self.doc
