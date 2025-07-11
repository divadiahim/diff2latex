import sys
import difflib
from itertools import zip_longest

HEADER = r"""
\documentclass{article}
\usepackage[table]{xcolor}
\usepackage{tabularx}
\usepackage[margin=1in]{geometry}
\usepackage{courier}
\usepackage{fvextra} % Better minted inside tables
\usepackage{comment}
\usepackage{listings}
\usepackage{ltablex}
\usepackage{fontspec}
\keepXColumns
"""

COLORS = r"""
\definecolor{addgreen}{RGB}{220,255,220}
\definecolor{remred}{RGB}{255,220,220}
\definecolor{diffchargreen}{RGB}{180,250,180} % inline change
\definecolor{diffcharred}{RGB}{250,180,180} % inline change
\definecolor{lightgray}{gray}{0.95}
"""

LISTINGS_CONFIG = r"""
\lstdefinestyle{diffcode}{
    basicstyle=\fontencoding{T1}\fontfamily{SourceSansPro-TLF}\selectfont\small,
    upquote=true,
    backgroundcolor=\color{lightgray},
    language=Python,
    showstringspaces=false,
    breaklines=true
}
"""

BOX_CONFIG = r"""
\setlength{\fboxsep}{0pt}  % inner padding
\setlength{\fboxrule}{0pt} % border thickness
\newfontfamily\sourcesanspro{Source Sans Pro}
\newcommand{\boxx}[2]{%
  \fcolorbox{#1}{#1}{%
    \small%
    \sourcesanspro%
    \strut #2%
  }%
}
"""

CODE_CONFIG = r"""
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcommand{\code}[1]{\lstinline[style=diffcode]§#1§}
"""


def make_document(content):
    return (
        r"""
\begin{document}
\begin{tabularx}{\linewidth}{r Y r Y}
\multicolumn{1}{c}{\textbf{\#}} & \multicolumn{1}{c}{\textbf{Old Code}} &
\multicolumn{1}{c}{\textbf{\#}} & \multicolumn{1}{c}{\textbf{New Code}} \\
\hline
%s
\hline
\end{tabularx}
\end{document}
"""
        % content
    )


def sanitize(s):
    """Sanitize string for LaTeX."""
    return (
        s.replace("\\", "\\textbackslash{}")
        .replace("%", "\\%")
        .replace("$", "\\$")
        .replace("&", "\\&")
        .replace("  ", "\\ \\ ")
        .replace("_", "\\_")
        .replace("{", "\\{")
        .replace("}", "\\}")
        .replace("#", "\\#")
    )


def inline_diff(old_line, new_line):
    old_indent = len(old_line) - len(old_line.lstrip())
    new_indent = len(new_line) - len(new_line.lstrip())

    old_tokens = old_line.lstrip().split()
    new_tokens = new_line.lstrip().split()
    matcher = difflib.SequenceMatcher(None, old_tokens, new_tokens)

    old_chunks = []
    new_chunks = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old_part = " ".join(sanitize(tok) for tok in old_tokens[i1:i2])
        new_part = " ".join(sanitize(tok) for tok in new_tokens[j1:j2])

        if tag == "equal":
            if old_part:
                old_chunks.append(f"\\code{{{old_part}}}")
                new_chunks.append(f"\\code{{{new_part}}}")
        elif tag == "replace":
            if old_part:
                old_chunks.append(f"\\boxx{{diffcharred}}{{{old_part}}}")
            if new_part:
                new_chunks.append(f"\\boxx{{diffchargreen}}{{{new_part}}}")
        elif tag == "delete":
            if old_part:
                old_chunks.append(f"\\boxx{{diffcharred}}{{{old_part}}}")
        elif tag == "insert":
            if new_part:
                new_chunks.append(f"\\boxx{{diffchargreen}}{{{new_part}}}")

    old_indent_str = "\\ " * old_indent if old_indent > 0 else ""
    new_indent_str = "\\ " * new_indent if new_indent > 0 else ""

    old_result = old_indent_str + " ".join(old_chunks)
    new_result = new_indent_str + " ".join(new_chunks)
    return old_result, new_result


def flush_hunk(hunk):
    old_lineno = new_lineno = 1
    paired = []
    deletions = [line[1:].rstrip() for line in hunk if line.startswith("-")]
    additions = [line[1:].rstrip() for line in hunk if line.startswith("+")]
    max_len = max(len(deletions), len(additions))

    for i in range(max_len):
        old_line = deletions[i] if i < len(deletions) else ""
        new_line = additions[i] if i < len(additions) else ""

        if old_line and new_line:
            old_diff, new_diff = inline_diff(old_line, new_line)
            paired.append(
                (
                    f"\\cellcolor{{remred}}{old_lineno}",
                    f"\\cellcolor{{remred}}{old_diff}",
                    f"\\cellcolor{{addgreen}}{new_lineno}",
                    f"\\cellcolor{{addgreen}}{new_diff}",
                )
            )
            old_lineno += 1
            new_lineno += 1
        elif old_line:
            paired.append(
                (
                    f"\\cellcolor{{remred}}{old_lineno}",
                    f"\\cellcolor{{remred}}\\code{{{sanitize(old_line)}}}",
                    "",
                    "",
                )
            )
            old_lineno += 1
        elif new_line:
            paired.append(
                (
                    "",
                    "",
                    f"\\cellcolor{{addgreen}}{new_lineno}",
                    f"\\cellcolor{{addgreen}}\\code{{{sanitize(new_line)}}}",
                )
            )
            new_lineno += 1
    return paired


def parse_diff_lines(diff_lines):
    rows = []
    old_lineno = new_lineno = 1
    hunk = []

    for line in diff_lines:
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            continue
        elif line.startswith("-") or line.startswith("+"):
            hunk.append(line)
        else:
            if hunk:
                rows.extend(flush_hunk(hunk))
                hunk = []

            content = line[1:].rstrip() if line.startswith(" ") else line.rstrip()
            rows.append(
                (
                    str(old_lineno),
                    f"\\code{{{sanitize(content)}}}",
                    str(new_lineno),
                    f"\\code{{{sanitize(content)}}}",
                )
            )
            old_lineno += 1
            new_lineno += 1

    if hunk:
        rows.extend(flush_hunk(hunk))

    return rows


def generate_latex_table(diff_rows):
    content = []

    for row in diff_rows:
        content.append(" & ".join(str(col) for col in row) + " \\\\")

    latex = [
        HEADER,
        COLORS,
        LISTINGS_CONFIG,
        CODE_CONFIG,
        BOX_CONFIG,
        make_document("\n".join(content)),
    ]

    return "\n".join(latex)


def main(diff_file_path):
    with open(diff_file_path, "r") as f:
        diff_lines = f.readlines()

    diff_rows = parse_diff_lines(diff_lines)
    latex_table = generate_latex_table(diff_rows)

    print(latex_table)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python diff_to_latex.py <language> <diff_file>")
        sys.exit(1)
    main(sys.argv[2])
