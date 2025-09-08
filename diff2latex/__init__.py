"""diff2latex - A simple utility that produces github-styled diffs in a synthesizable LaTeX format."""

__version__ = "0.1.0"
__author__ = "divadiahim"

# Import main classes for easy access
from .cli import main
from .core.diff2latex import Diff2Latex
from .core.models import CodeBlock, Cell, Line
from .core.utils import CharColorizer, ColorMap

# Import convenience API
from .api import (
    diff_to_latex,
    diff_file_to_latex,
    create_diff_pdf,
    DiffProcessor,
)

# Export all important classes and functions
__all__ = [
    # CLI
    "main",
    # Metadata
    "__version__",
    "__author__",
    # Core classes
    "Diff2Latex",
    # Model classes
    "CodeBlock",
    "Cell", 
    "Line",
    # Utility classes
    "CharColorizer",
    "ColorMap",
    # Convenience API
    "diff_to_latex",
    "diff_file_to_latex", 
    "create_diff_pdf",
    "DiffProcessor",
]

if __name__ == "__main__":
    main()