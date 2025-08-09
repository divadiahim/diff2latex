# diff2latex

A simple utility that produces github-styled diffs in a synthesizable LaTeX format.

## Requirements

- `lualatex` for pdf generation
- `python`
- `diff`

## Installation

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

- Grab 2 files that you want to diff and generate a plain diff `diff -u file_1 file_2 > example.diff`.
- To generate a LaTeX diff run `diff2latex --highlight="default" build example.diff output`. This will create a directory named `output` containing `example.tex`.
- To additionally generate a pdf pass the `--build-pdf` flag.

## TODOs

- [ ] Add a horizontal diff style.
