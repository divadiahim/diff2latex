"""
Convenience module for common diff2latex operations.

This module provides high-level functions for the most common use cases.
"""

from typing import TextIO, Optional
from pathlib import Path
import tempfile
import os

from .core.diff2latex import Diff2Latex
from .core.utils import CharColorizer


def diff_to_latex(
    diff_content: str,
    output_path: Optional[str] = None,
    font_family: str = "Fira Code",
    font_size: str = "10pt",
    highlight_style: Optional[str] = None,
    file_extension: Optional[str] = None
) -> str:
    """
    Convert diff content to LaTeX format.
    
    Args:
        diff_content: The diff content as a string
        output_path: Optional path to write the LaTeX output
        font_family: Font family for the LaTeX document
        font_size: Font size for the LaTeX document  
        highlight_style: Pygments style for syntax highlighting
        file_extension: File extension to determine lexer for highlighting
    
    Returns:
        The LaTeX content as a string
    
    Example:
        >>> diff_content = '''
        ... --- file1.txt
        ... +++ file2.txt
        ... @@ -1,3 +1,3 @@
        ...  line 1
        ... -old line 2
        ... +new line 2
        ...  line 3
        ... '''
        >>> latex = diff_to_latex(diff_content)
        >>> print(latex[:50])
    """
    from io import StringIO
    from string import Template
    
    # Create colorizer
    colorizer = CharColorizer(
        style_name=highlight_style,
        ext=file_extension
    )
    
    # Convert diff to LaTeX
    diff_io = StringIO(diff_content)
    differ = Diff2Latex.build(diff_io, colorizer=colorizer)
    latex_content = differ.to_latex()
    
    # Load template
    template_path = os.path.join(os.path.dirname(__file__), "templates", "template.tex")
    with open(template_path, "r") as f:
        template = Template(f.read())
    
    # Generate final LaTeX
    final_latex = template.substitute(
        font=font_family,
        fontsize=font_size,
        content=latex_content,
    )
    
    # Write to file if requested
    if output_path:
        with open(output_path, "w") as f:
            f.write(final_latex)
    
    return final_latex


def diff_file_to_latex(
    diff_file_path: str,
    output_path: Optional[str] = None,
    **kwargs
) -> str:
    """
    Convert a diff file to LaTeX format.
    
    Args:
        diff_file_path: Path to the diff file
        output_path: Optional path to write the LaTeX output
        **kwargs: Additional arguments passed to diff_to_latex()
    
    Returns:
        The LaTeX content as a string
    
    Example:
        >>> latex = diff_file_to_latex("my_changes.diff", "output.tex")
    """
    with open(diff_file_path, "r") as f:
        diff_content = f.read()
    
    return diff_to_latex(diff_content, output_path, **kwargs)


def create_diff_pdf(
    diff_content: str,
    output_pdf_path: str,
    **kwargs
) -> None:
    """
    Create a PDF from diff content using lualatex.
    
    Args:
        diff_content: The diff content as a string
        output_pdf_path: Path where the PDF should be saved
        **kwargs: Additional arguments passed to diff_to_latex()
    
    Raises:
        RuntimeError: If lualatex is not found in PATH
    
    Example:
        >>> create_diff_pdf(diff_content, "my_diff.pdf", highlight_style="github")
    """
    import shutil
    import subprocess
    
    if shutil.which("lualatex") is None:
        raise RuntimeError("lualatex not found in PATH. Please install it.")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate LaTeX
        tex_path = os.path.join(tmpdir, "temp.tex")
        latex_content = diff_to_latex(diff_content, tex_path, **kwargs)
        
        # Compile to PDF
        subprocess.run(
            ["lualatex", "-interaction=nonstopmode", tex_path],
            cwd=tmpdir,
            check=True
        )
        subprocess.run(
            ["lualatex", "-interaction=nonstopmode", tex_path], 
            cwd=tmpdir,
            check=True
        )
        
        # Move PDF to final location
        temp_pdf = os.path.join(tmpdir, "temp.pdf")
        shutil.move(temp_pdf, output_pdf_path)


class DiffProcessor:
    """
    A class-based interface for processing diffs.
    
    This provides a more object-oriented approach for repeated diff processing.
    
    Example:
        >>> processor = DiffProcessor(
        ...     font_family="Monaco",
        ...     highlight_style="monokai"
        ... )
        >>> latex1 = processor.process(diff_content1)
        >>> latex2 = processor.process(diff_content2)
    """
    
    def __init__(
        self,
        font_family: str = "Fira Code",
        font_size: str = "10pt",
        highlight_style: Optional[str] = None,
        file_extension: Optional[str] = None
    ):
        """
        Initialize the diff processor with default settings.
        
        Args:
            font_family: Default font family
            font_size: Default font size
            highlight_style: Default highlighting style
            file_extension: Default file extension for lexer detection
        """
        self.font_family = font_family
        self.font_size = font_size
        self.highlight_style = highlight_style
        self.file_extension = file_extension
        
        # Create colorizer
        self.colorizer = CharColorizer(
            style_name=highlight_style,
            ext=file_extension
        )
    
    def process(
        self,
        diff_content: str,
        output_path: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Process diff content to LaTeX.
        
        Args:
            diff_content: The diff content
            output_path: Optional output path
            **kwargs: Override default settings
        
        Returns:
            LaTeX content as string
        """
        # Override defaults with any provided kwargs
        settings = {
            'font_family': self.font_family,
            'font_size': self.font_size,
            'highlight_style': self.highlight_style,
            'file_extension': self.file_extension,
        }
        settings.update(kwargs)
        
        return diff_to_latex(diff_content, output_path, **settings)
    
    def process_file(self, diff_file_path: str, output_path: Optional[str] = None, **kwargs) -> str:
        """Process a diff file to LaTeX."""
        with open(diff_file_path, "r") as f:
            diff_content = f.read()
        return self.process(diff_content, output_path, **kwargs)
    
    def create_pdf(self, diff_content: str, output_pdf_path: str, **kwargs) -> None:
        """Create a PDF from diff content."""
        # Override defaults
        settings = {
            'font_family': self.font_family,
            'font_size': self.font_size,
            'highlight_style': self.highlight_style,
            'file_extension': self.file_extension,
        }
        settings.update(kwargs)
        
        create_diff_pdf(diff_content, output_pdf_path, **settings)
