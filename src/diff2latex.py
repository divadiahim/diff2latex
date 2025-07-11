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
    basicstyle=\fontencoding{T1}\selectfont\small\ttfamily,
    upquote=true,
    backgroundcolor=\color{lightgray},
    language=Python,
    showstringspaces=false,
    breaklines=true
}
"""

CODE_CONFIG = r"""
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\newcommand{\code}[1]{\lstinline[style=diffcode]§#1§}
\setlength{\fboxsep}{0pt}  % inner padding
\setlength{\fboxrule}{0pt} % border thickness
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
    matcher = difflib.SequenceMatcher(None, old_line, new_line)
    old_chunks = []
    new_chunks = []

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        old_part = sanitize(old_line[i1:i2])
        new_part = sanitize(new_line[j1:j2])

        if tag == 'equal':
            if old_part:
                old_chunks.append(f"\\code{{{old_part}}}")
                new_chunks.append(f"\\code{{{new_part}}}")
        elif tag == 'replace':
            if old_part:
                old_chunks.append(f"\\fcolorbox{{diffcharred}}{{diffcharred}}{{\\small\\ttfamily{{{old_part}}}}}")
            if new_part:
                new_chunks.append(f"\\fcolorbox{{diffchargreen}}{{diffchargreen}}{{\\small\\ttfamily{{{new_part}}}}}")
        elif tag == 'delete':
            if old_part:
                old_chunks.append(f"\\fcolorbox{{diffcharred}}{{diffcharred}}{{\\small\\ttfamily{{{old_part}}}}}")
        elif tag == 'insert':
            if new_part:
                new_chunks.append(f"\\fcolorbox{{diffchargreen}}{{diffchargreen}}{{\\small\\ttfamily{{{new_part}}}}}")

    return ''.join(old_chunks), ''.join(new_chunks)


def parse_diff_lines(diff_lines):
    old_code = []
    new_code = []
    old_lineno = new_lineno = 1
    rows = []

    for line in diff_lines:
        if line.startswith("---") or line.startswith("+++") or line.startswith("@@"):
            continue
        if line.startswith("-"):
            content = line[1:].rstrip()
            rows.append((old_lineno, (content), "", "", "remred"))
            old_code.append(content)
            old_lineno += 1
        elif line.startswith("+"):
            content = line[1:].rstrip()
            rows.append(("", "", new_lineno, (content), "addgreen"))
            new_code.append(content)
            new_lineno += 1
        else:
            content = line[1:].rstrip() if line.startswith(" ") else line.rstrip()
            rows.append((old_lineno, (content), new_lineno, (content), ""))
            old_code.append(content)
            new_code.append(content)
            old_lineno += 1
            new_lineno += 1

    # Detect inline changes
    processed_rows = []
    row_map = {}
    left = right = 0
    for row in rows:
        old_n, old_val, new_n, new_val, color = row
        if old_n and not new_n:
            processed_rows.append(
                (
                    f"\\cellcolor{{remred}}{old_n}",
                    f"\\cellcolor{{remred}}\\code{{{sanitize(old_val)}}}",
                    "",
                    "",
                )
            )
            row_map[left] = row
            left += 1
        elif not old_n and new_n:
            # processed_rows[right] = processed_rows[right][:2] + (f"\\cellcolor{{addgreen}}{new_n}", f"\\cellcolor{{addgreen}}\\code{{{sanitize(new_val)}}}")
            local_old_n, local_old_val, _, _, _ = row_map[left - 1]
            old_diff, new_diff = inline_diff(local_old_val, new_val)
            processed_rows[right] = (
                f"\\cellcolor{{remred}}{local_old_n}",
                f"\\cellcolor{{remred}}{old_diff}",
                f"\\cellcolor{{addgreen}}{new_n}",
                f"\\cellcolor{{addgreen}}{new_diff}",
            )
            right += 1
        else:
            processed_rows.append(
                (
                    old_n,
                    f"\\code{{{sanitize(old_val)}}}",
                    new_n,
                    f"\\code{{{sanitize(new_val)}}}",
                )
            )
            left += 1
            right = left

    return processed_rows


def generate_latex_table(diff_rows):
    content = []

    for row in diff_rows:
        content.append(" & ".join(str(col) for col in row) + " \\\\")
        
    latex = [
        HEADER,
        COLORS,
        LISTINGS_CONFIG,
        CODE_CONFIG,
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
