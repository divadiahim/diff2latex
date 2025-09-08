# diff2latex Library Usage Guide

## Quick Start

### Installation

```bash
pip install diff2latex
```

### Basic Usage

```python
import diff2latex

# Convert diff content to LaTeX
diff_content = """--- old.py
+++ new.py
@@ -1,2 +1,2 @@
-print("Hello")  
+print("Hello, World!")
"""

latex = diff2latex.diff_to_latex(diff_content, highlight_style="github")
print(latex)
```

## API Reference

### Functions

#### `diff2latex.diff_to_latex(diff_content, **kwargs)`

Convert diff content (string) to LaTeX format.

**Parameters:**
- `diff_content` (str): The diff content as a string
- `output_path` (str, optional): Path to write LaTeX output
- `font_family` (str): Font family (default: "Fira Code")
- `font_size` (str): Font size (default: "10pt")
- `highlight_style` (str, optional): Pygments style for syntax highlighting
- `file_extension` (str, optional): File extension for lexer detection

**Returns:** LaTeX content as string

#### `diff2latex.diff_file_to_latex(diff_file_path, **kwargs)`

Convert a diff file to LaTeX format.

**Parameters:**
- `diff_file_path` (str): Path to the diff file
- `output_path` (str, optional): Path to write LaTeX output
- `**kwargs`: Additional arguments passed to `diff_to_latex()`

**Returns:** LaTeX content as string

#### `diff2latex.create_diff_pdf(diff_content, output_pdf_path, **kwargs)`

Create a PDF from diff content using lualatex.

**Parameters:**
- `diff_content` (str): The diff content as a string
- `output_pdf_path` (str): Path where the PDF should be saved
- `**kwargs`: Additional arguments passed to `diff_to_latex()`

**Raises:** `RuntimeError` if lualatex is not found in PATH

### Classes

#### `diff2latex.DiffProcessor`

A class-based interface for processing multiple diffs with consistent settings.

```python
processor = diff2latex.DiffProcessor(
    font_family="Monaco",
    font_size="9pt", 
    highlight_style="monokai",
    file_extension=".py"
)

# Process multiple diffs
latex1 = processor.process(diff_content1)
latex2 = processor.process(diff_content2)

# Create PDFs
processor.create_pdf(diff_content1, "output1.pdf")
processor.create_pdf(diff_content2, "output2.pdf")
```

**Methods:**
- `process(diff_content, output_path=None, **kwargs)`: Process diff content
- `process_file(diff_file_path, output_path=None, **kwargs)`: Process diff file
- `create_pdf(diff_content, output_pdf_path, **kwargs)`: Create PDF

#### Core Classes (Advanced Usage)

For advanced usage, you can import and use the core classes directly:

- `diff2latex.Diff2Latex`: Main diff processing class
- `diff2latex.CharColorizer`: Syntax highlighting utilities
- `diff2latex.ColorMap`: Color mapping utilities  
- `diff2latex.CodeBlock`: Represents a code block
- `diff2latex.Cell`: Represents a table cell
- `diff2latex.Line`: Represents a diff line

```python
from diff2latex import Diff2Latex, CharColorizer
from io import StringIO

colorizer = CharColorizer(style_name="github", ext=".py")
diff_io = StringIO(diff_content)
differ = Diff2Latex.build(diff_io, colorizer=colorizer)
latex_lines = differ.to_latex()
```

## Examples

### Example 1: Simple Conversion

```python
import diff2latex

diff = """--- README.md
+++ README.md
@@ -1,4 +1,4 @@
 # My Project
 
-This is the old description.
+This is the new description.
 
"""

latex = diff2latex.diff_to_latex(diff, output_path="readme_changes.tex")
```

### Example 2: Python Code with Syntax Highlighting

```python
import diff2latex

python_diff = """--- main.py
+++ main.py
@@ -1,5 +1,6 @@
 def main():
+    print("Starting application...")
     data = load_data()
-    process(data)
+    result = process(data)
+    save_result(result)
"""

latex = diff2latex.diff_to_latex(
    python_diff,
    highlight_style="github",
    file_extension=".py"
)
```

### Example 3: Batch Processing

```python
from diff2latex import DiffProcessor
import os

processor = DiffProcessor(
    font_family="Source Code Pro",
    highlight_style="vs"
)

# Process all diff files in a directory
for filename in os.listdir("diffs/"):
    if filename.endswith(".diff"):
        input_path = f"diffs/{filename}"
        output_path = f"latex/{filename}.tex"
        
        processor.process_file(input_path, output_path)
```

### Example 4: PDF Generation

```python
import diff2latex

# Generate PDF directly
diff2latex.create_diff_pdf(
    diff_content,
    "my_changes.pdf",
    highlight_style="github",
    font_family="Monaco"
)
```

## Supported Highlight Styles

Common Pygments styles you can use:
- `"github"` - GitHub-style highlighting
- `"monokai"` - Monokai theme
- `"vs"` - Visual Studio style
- `"colorful"` - Colorful theme
- `"default"` - Default Pygments style
- `None` - No syntax highlighting

## Supported File Extensions

The library can auto-detect lexers for:
- `.py` - Python
- `.cpp`, `.c`, `.cc`, `.cxx`, `.h`, `.hpp` - C/C++
- `.java` - Java
- `.hs` - Haskell

## Requirements

- Python 3.7+
- Dependencies: click, pydantic, Pygments, typing-extensions
- For PDF generation: `lualatex` (from TeX Live or similar)

## Error Handling

```python
import diff2latex

try:
    # This will raise RuntimeError if lualatex is not available
    diff2latex.create_diff_pdf(diff_content, "output.pdf")
except RuntimeError as e:
    print(f"PDF generation failed: {e}")
    # Fallback to LaTeX only
    latex = diff2latex.diff_to_latex(diff_content, output_path="output.tex")
```
