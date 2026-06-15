"""
Template registry — maps style names to their renderer classes.

To add a new template:
  1. Create a folder: doc_maker/templates/<your_style>/
  2. Add theme.py (colours/config) and renderer.py (subclass of BaseRenderer)
  3. Import and register it here with one line.
"""

from .pearson_edexcel.renderer import PearsonEdexcelRenderer

REGISTRY: dict[str, type] = {
    "pearson-edexcel": PearsonEdexcelRenderer,
}

DEFAULT_STYLE = "pearson-edexcel"
