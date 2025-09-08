# diff2latex

A simple utility that produces github-styled diffs in a synthesizable LaTeX format.

## Requirements

- `lualatex` for pdf generation (optional, only needed for PDF output)
- `python` 3.7+

## Installation

### From PyPI (recommended)

```sh
pip install diff2latex
```

### From source

1. Clone this repository
   ```sh
   git clone https://github.com/divadiahim/diff2latex.git
   cd diff2latex
   ```
2. Install dependencies and build the package
   ```sh
   pip install -r requirements.txt
   pip install -e .
   ```

## Usage

### Command Line Interface

- Grab 2 files that you want to diff and generate a plain diff `diff -u file_1 file_2 > example.diff`.
- To generate a LaTeX diff run `diff2latex --highlight="default" build example.diff output`. This will create a directory named `output` containing `example.tex`.
- To additionally generate a pdf pass the `--pdf-output` flag.

### Library Usage

You can also use diff2latex as a Python library for programmatic diff processing:

#### Simple Usage

```python
import diff2latex

# Convert diff content to LaTeX
diff_content = """--- old.py
+++ new.py
@@ -1,2 +1,2 @@
-print("Hello")
+print("Hello, World!")
"""

latex_output = diff2latex.diff_to_latex(
    diff_content,
    highlight_style="github",
    file_extension=".py"
)

# Save to file
with open("output.tex", "w") as f:
    f.write(latex_output)

# Or create PDF directly
diff2latex.create_diff_pdf(diff_content, "output.pdf", highlight_style="github")
```

#### Class-based Processing

```python
from diff2latex import DiffProcessor

# Create processor with default settings
processor = DiffProcessor(
    font_family="Monaco",
    highlight_style="monokai",
    file_extension=".cpp"
)

# Process multiple diffs with consistent styling
latex1 = processor.process(diff_content1)
latex2 = processor.process(diff_content2)

# Create PDFs
processor.create_pdf(diff_content1, "diff1.pdf")
processor.create_pdf(diff_content2, "diff2.pdf")
```

#### Advanced Usage

```python
from diff2latex import Diff2Latex, CharColorizer
from io import StringIO

# Use core classes directly
colorizer = CharColorizer(style_name="github", ext=".py")
diff_io = StringIO(diff_content)
differ = Diff2Latex.build(diff_io, colorizer=colorizer)
latex_lines = differ.to_latex()
```

#### Available Functions

- `diff2latex.diff_to_latex(content, **kwargs)` - Convert diff string to LaTeX
- `diff2latex.diff_file_to_latex(file_path, **kwargs)` - Convert diff file to LaTeX  
- `diff2latex.create_diff_pdf(content, output_path, **kwargs)` - Create PDF directly
- `diff2latex.DiffProcessor(**kwargs)` - Class-based processor for multiple diffs

#### Available Classes

All core classes are importable for advanced usage:
- `Diff2Latex` - Main diff processing class
- `CharColorizer` - Syntax highlighting
- `ColorMap` - Color mapping utilities
- `CodeBlock`, `Cell`, `Line` - Data models

See `examples.py` for more detailed usage examples.

## Development

### Setting up development environment

```sh
# Clone the repository
git clone https://github.com/divadiahim/diff2latex.git
cd diff2latex

# Run the development setup script
./setup_dev.sh

# Or manually:
pip install -e .
pip install -r requirements.txt
```

### Testing

Run the smoke tests to ensure everything works:

```sh
python test_package.py
```

### Publishing

1. Update the version in `diff2latex/__init__.py`
2. Build and check the package:
   ```sh
   ./publish.sh
   ```
3. Upload to PyPI:
   ```sh
   # Test on TestPyPI first (recommended)
   python -m twine upload --repository testpypi dist/*
   
   # Then upload to PyPI
   python -m twine upload dist/*
   ```

## TODOs

- [ ] Add a horizontal diff style.
- [ ] Add comprehensive unit tests
- [ ] Add GitHub Actions CI/CD
- [ ] Add documentation with examples
