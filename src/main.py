import sys
import difflib
from itertools import zip_longest

HEADER = r"""
\documentclass{article}
\usepackage[table]{xcolor}
\usepackage{tabularx}
\usepackage{minted2}
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
\definecolor{diffchar}{RGB}{180,250,180} % inline change
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
\newcommand{\code}[1]{\lstinline[style=diffcode]!#1!}
"""


def make_document(content):
    return (
        r"""
\begin{tabularx}{\linewidth}{r X r X}
\multicolumn{1}{c}{\textbf{\#}} & \multicolumn{1}{c}{\textbf{Old Code}} &
\multicolumn{1}{c}{\textbf{\#}} & \multicolumn{1}{c}{\textbf{New Code}} \\
\hline
%s
\end{tabularx}
\end{document}
"""
        % content
    )


def inline_diff(old_line, new_line):
    matcher = difflib.SequenceMatcher(None, old_line, new_line)
    old_parts, new_parts = "", ""
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            old_parts += old_line[i1:i2]
            new_parts += new_line[j1:j2]
        elif tag == "replace":
            old_parts += (
                f"\\fcolorbox{{diffchar}}{{diffchar}}{{\\ttfamily {(old_line[i1:i2])}}}"
            )
            new_parts += (
                f"\\fcolorbox{{diffchar}}{{diffchar}}{{\\ttfamily {(new_line[j1:j2])}}}"
            )
        elif tag == "delete":
            old_parts += (
                f"\\fcolorbox{{diffchar}}{{diffchar}}{{\\ttfamily {(old_line[i1:i2])}}}"
            )
        elif tag == "insert":
            new_parts += (
                f"\\fcolorbox{{diffchar}}{{diffchar}}{{\\ttfamily {(new_line[j1:j2])}}}"
            )
    return old_parts, new_parts


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
    left = right = 0
    for row in rows:
        old_n, old_val, new_n, new_val, color = row
        # if old_n and new_n and old_val != new_val:
        #     old_diff, new_diff = inline_diff(old_val, new_val)
        #     processed_rows.append((f"\\cellcolor{{remred}}{old_n}", f"\\cellcolor{{remred}}\\code{{{old_diff}}}",
        #                            f"\\cellcolor{{addgreen}}{new_n}", f"\\cellcolor{{addgreen}}\\code{{{new_diff}}}"))
        # elif old_n and not new_n:  # Removed
        #     processed_rows.append((f"\\cellcolor{{remred}}{old_n}", f"\\cellcolor{{remred}}\\code{{{old_val.replace(" ", "\\ ")}}}", "", ""))
        # elif not old_n and new_n:  # Added
        #     processed_rows.append(("", "", f"\\cellcolor{{addgreen}}{new_n}", f"\\cellcolor{{addgreen}}\\code{{{new_val.replace(" ", "\\ ")}}}"))
        # else:  # Unchanged
        #     processed_rows.append((old_n, f"\\code{{{old_val}}}", new_n, f"\\code{{{new_val}}}"))
        if old_n and not new_n:
            processed_rows.append(
                (
                    f"\\cellcolor{{remred}}{old_n}",
                    f"\\cellcolor{{remred}}\\code{{{sanitize(old_val)}}}",
                    "",
                    "",
                )
            )
            left += 1
        elif not old_n and new_n:
            # processed_rows[right] = processed_rows[right][:2] + (f"\\cellcolor{{addgreen}}{new_n}", f"\\cellcolor{{addgreen}}\\code{{{sanitize(new_val)}}}")
            old_diff, new_diff = inline_diff(old_val, new_val)
            processed_rows[right] = (
                f"\\cellcolor{{remred}}{old_n}",
                f"\\cellcolor{{remred}}\\code{{{old_diff}}}",
                f"\\cellcolor{{addgreen}}{new_n}",
                f"\\cellcolor{{addgreen}}\\code{{{new_diff}}}",
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
    # latex = [
    #     "\\begin{tabularx}{\\linewidth}{r X r X}",
    #     "\\multicolumn{1}{c}{\\textbf{\\#}} & \\multicolumn{1}{c}{\\textbf{Old Code}} &",
    #     "\\multicolumn{1}{c}{\\textbf{\\#}} & \\multicolumn{1}{c}{\\textbf{New Code}} \\\\",
    #     "\\hline",
    # ]
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
        
    # content.append("\\hline\n\\end{tabularx}")
    return "\n".join(latex)


def main(diff_file_path):
    with open(diff_file_path, "r") as f:
        diff_lines = f.readlines()

    diff_rows = parse_diff_lines(diff_lines)
    latex_table = generate_latex_table(diff_rows)

    print(latex_table)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python diff_to_latex.py <language> <diff_file>")
        sys.exit(1)
    main(sys.argv[1])
