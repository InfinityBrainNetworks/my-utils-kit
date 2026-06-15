"""
IBN Codexis Computer Science Textbook — colour theme and directive config.

Flat design: no coloured boxes. Structure is created entirely through
typography (size, weight, colour) and paragraph borders.

Source: IBN_Codexis_G11_Ch1_Programming.docx
"""

# ── colour palette ─────────────────────────────────────────────────────────────
PRIMARY      = "1A5276"   # deep blue   — "What You Will Learn", bold labels, figure captions
ACCENT       = "2471A3"   # medium blue — section/sub-section heading text + borders
BODY         = "2C3E50"   # dark slate  — all body text
CAPTION      = "5D6D7E"   # grey-blue   — table / code / pseudo-code captions (italic, small)
BORDER_SOFT  = "D6EEF8"   # pale blue   — thin bottom border on sub-section headings (H3)
BORDER_H2    = "1A5276"   # deep blue   — bottom border on major section headings (H2)
QUESTION_CLR = "1B2631"   # near-black  — question text in exercises / review sections

# ── heading sizes (pt) ────────────────────────────────────────────────────────
H2_PT   = 16.0    # major section  (1.1, 1.2 …)       left+bottom border
H3_PT   = 12.0    # sub-section    (1.2.1, …)          bottom border only
H4_PT   = 10.5    # sub-sub-head   (Variables, i. …)   no border
H5_PT   = 10.0    # labelled item  (Assembler, …)       no border

# ── directive config: name → (display label, label colour, label pt) ──────────
# These are "flat" label blocks — a styled header line followed by body content.
# No coloured box or shading. The label appears in PRIMARY colour, bold.
LABEL_DIRECTIVES: dict[str, tuple[str, str, float]] = {
    "learning-objectives": ("WHAT YOU WILL LEARN",                PRIMARY, 13.0),
    "section-goals":       ("IN THIS SECTION YOU WILL LEARN TO",  PRIMARY, 10.0),
    "chapter-summary":     ("CHAPTER SUMMARY",                    PRIMARY, 13.0),
    "key-terms":           ("KEY TERMS GLOSSARY",                 PRIMARY, 13.0),
    "review-questions":    ("REVIEW QUESTIONS",                   PRIMARY, 13.0),
    "worked-examples":     ("WORKED EXAMPLES",                    PRIMARY, 10.5),
    "section-a":           ("Section A — Short Answer Questions", PRIMARY, 11.0),
    "section-b":           ("Section B — Structured Questions",   PRIMARY, 11.0),
}
