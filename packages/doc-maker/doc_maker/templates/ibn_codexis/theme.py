"""
IBN Codexis Computer Science Textbook — colour theme and directive config.

All colours extracted directly from IBN_Codexis_G11_Ch1_Programming.docx:
  - Boxes are Word tables: dark header row + light body row
  - Data tables use blue header (#1A5276) + white text
  - Code blocks use a dark VS-Code-style background (#1E1E2E)
"""

# ── heading / body colours ─────────────────────────────────────────────────────
PRIMARY      = "1A5276"   # deep blue   — chapter title, figure captions, labels
ACCENT       = "2471A3"   # medium blue — H2/H3 heading text + borders
BODY         = "2C3E50"   # dark slate  — body paragraphs
CAPTION      = "5D6D7E"   # grey-blue   — table/code captions, subtitle, footer
BORDER_SOFT  = "D6EEF8"   # pale blue   — thin bottom border on H3
BORDER_H2    = "1A5276"   # deep blue   — bottom border on H2

# ── heading sizes (pt) ────────────────────────────────────────────────────────
H2_PT   = 16.0   # major section  (1.1 …)     left+bottom border
H3_PT   = 12.0   # sub-section    (1.2.1 …)   bottom border only
H4_PT   = 10.5   # sub-sub-head               no border
H5_PT   = 10.0   # labelled item              no border

# ── coloured box colours (from docx table cell fills) ─────────────────────────
BOX_FONT_HDR   = "FFFFFF"   # white — all box header text
BOX_FONT_BODY  = "1B2631"   # near-black — most box body text

KEY_TERM_HDR       = "1E8449"   # dark green
KEY_TERM_BODY      = "E9F7EF"   # light green

WORKED_EX_HDR      = "7D6608"   # dark olive/gold
WORKED_EX_BODY     = "FEF9E7"   # light cream

ACTIVITY_HDR       = "0E6655"   # dark teal
ACTIVITY_BODY      = "E8F8F5"   # light mint

REMEMBER_HDR       = "154360"   # dark navy
REMEMBER_BODY      = "D6EAF8"   # light blue

EXAM_TIP_HDR       = "784212"   # dark brown/amber
EXAM_TIP_BODY      = "FEF5E7"   # light orange

DID_YOU_KNOW_HDR   = "4A235A"   # dark purple
DID_YOU_KNOW_BODY  = "F4ECF7"   # light lavender

# ── code block ────────────────────────────────────────────────────────────────
CODE_BG    = "1E1E2E"   # very dark (VS Code dark theme)
CODE_FONT  = "89B4FA"   # light blue — code text colour

# ── figure placeholder ────────────────────────────────────────────────────────
FIGURE_BG   = "F2F3F4"   # light grey
FIGURE_FONT = "626567"   # medium grey text

# ── data table header ─────────────────────────────────────────────────────────
TABLE_HDR   = "1A5276"   # same as PRIMARY — matches source

# ── box directive registry ────────────────────────────────────────────────────
# name → (display label, header fill, body fill)
BOX_DIRECTIVES: dict[str, tuple[str, str, str]] = {
    "key-term":      ("KEY TERM",      KEY_TERM_HDR,     KEY_TERM_BODY),
    "worked-example":("WORKED EXAMPLE", WORKED_EX_HDR,   WORKED_EX_BODY),
    "activity":      ("ACTIVITY",      ACTIVITY_HDR,     ACTIVITY_BODY),
    "remember":      ("REMEMBER",      REMEMBER_HDR,     REMEMBER_BODY),
    "exam-tip":      ("EXAM TIP",      EXAM_TIP_HDR,     EXAM_TIP_BODY),
    "did-you-know":  ("DID YOU KNOW?", DID_YOU_KNOW_HDR, DID_YOU_KNOW_BODY),
}

# ── flat label directives (end-of-chapter / structural) ───────────────────────
# name → (display label, label colour, label pt)
LABEL_DIRECTIVES: dict[str, tuple[str, str, float]] = {
    "learning-objectives": ("WHAT YOU WILL LEARN",               PRIMARY, 13.0),
    "section-goals":       ("IN THIS SECTION YOU WILL LEARN TO", PRIMARY, 10.0),
    "chapter-summary":     ("CHAPTER SUMMARY",                   PRIMARY, 13.0),
    "key-terms":           ("KEY TERMS GLOSSARY",                PRIMARY, 13.0),
    "review-questions":    ("REVIEW QUESTIONS",                  PRIMARY, 13.0),
    "worked-examples":     ("WORKED EXAMPLES",                   PRIMARY, 10.5),
    "section-a":           ("Section A — Short Answer Questions", PRIMARY, 11.0),
    "section-b":           ("Section B — Structured Questions",  PRIMARY, 11.0),
}
