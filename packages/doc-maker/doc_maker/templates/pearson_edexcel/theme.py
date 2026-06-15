"""
Pearson Edexcel Student Textbook — colour theme and directive config.

Each entry: directive-name → (box label, header hex fill, content hex fill)
"""

DIRECTIVE_CONFIG: dict[str, tuple[str, str, str]] = {
    # ── Page structure (elements 1–5) ─────────────────────────────────────────
    "learning-objectives":    ("LEARNING OBJECTIVES",    "1B5E8C", "D6E4F0"),
    "getting-started":        ("GETTING STARTED",         "1F6B42", "D9EFE3"),

    # ── Callout / info boxes (elements 6–15) ──────────────────────────────────
    "key-term":               ("KEY TERM",                "6A1B9A", "F3E5F5"),
    "key-terms":              ("KEY TERMS",               "6A1B9A", "F3E5F5"),
    "subject-vocabulary":     ("SUBJECT VOCABULARY",      "00695C", "E0F2F1"),
    "tip":                    ("TIP",                     "BF360C", "FBE9E7"),
    "exam-tip":               ("EXAM TIP",                "B71C1C", "FFEBEE"),
    "did-you-know":           ("DID YOU KNOW?",           "01579B", "E1F5FE"),
    "hint":                   ("HINT",                    "E65100", "FFF8E1"),
    "extend-your-knowledge":  ("EXTEND YOUR KNOWLEDGE",   "283593", "E8EAF6"),
    "maths-skills":           ("MATHS SKILLS",            "1565C0", "E3F2FD"),
    "skills-link":            ("SKILLS LINK",             "37474F", "ECEFF1"),
    "international-context":  ("INTERNATIONAL CONTEXT",   "1B5E20", "E8F5E9"),

    # ── Worked content (elements 16–17) ───────────────────────────────────────
    "worked-example":         ("WORKED EXAMPLE",          "004D40", "E0F2F1"),
    "worked-solution":        ("WORKED SOLUTION",         "006064", "E0F7FA"),

    # ── Exercise / assessment (elements 18–24) ────────────────────────────────
    "activity":               ("ACTIVITY",                "E65100", "FFF3E0"),
    "exercise":               ("EXERCISE",                "1A237E", "E8EAF6"),
    "checkpoint":             ("CHECKPOINT",              "4A148C", "F3E5F5"),
    "strengthen":             ("STRENGTHEN",              "1B5E20", "E8F5E9"),
    "challenge":              ("CHALLENGE",               "0D47A1", "E3F2FD"),
    "exam-style-questions":   ("EXAM-STYLE QUESTIONS",    "B71C1C", "FFEBEE"),
    "unit-questions":         ("UNIT QUESTIONS",          "4A148C", "EDE7F6"),

    # ── End of chapter (elements 25–26) ───────────────────────────────────────
    "chapter-summary":        ("CHAPTER SUMMARY",         "37474F", "ECEFF1"),
    "key-points":             ("KEY POINTS",              "1B5E20", "E8F5E9"),

    # ── Margin note (element 30) ───────────────────────────────────────────────
    "margin-note":            ("MARGIN NOTE",             "F57F17", "FFF9C4"),
}

# Chapter opener colours
ACCENT_COLOR    = "1B5E8C"   # Edexcel blue — rule, chapter label, title
SUBTITLE_COLOR  = "555555"   # dark grey — subtitle text
COVER_FILL      = "E8EDF2"   # light blue-grey — cover image placeholder background
