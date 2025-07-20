from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Tuple
from .models import Line, Cell, CodeBlock
from difflib import SequenceMatcher
import re


class Diff2Latex(BaseModel):
    _lines: List[Line] = PrivateAttr(default_factory=list)
    srclines: List[str] = Field(
        default_factory=list, description="Source lines from the diff file."
    )
    
    def _clean_diff_file(self) -> None:
        """Clean the diff file by removing unnecessary lines."""
        self.srclines = [line for line in self.srclines if not line.startswith(("---", "+++", "@@"))]

    def _tokenize(self, line: str) -> List[str]:
        """        Tokenize a line into words and special characters.
        This is a simple tokenizer that splits on whitespace and special characters.
        """
        return re.findall(r"\s+|\w+|[^\w\s]", line)

    def _inline_diff(self, old_line: str, new_line: str) -> Tuple[List[CodeBlock], List[CodeBlock]]:
        """        Perform an inline diff between two lines and return their LaTeX representations.
        """
        old_tokens = self._tokenize(old_line)
        new_tokens = self._tokenize(new_line)
        matcher = SequenceMatcher(None, old_tokens, new_tokens)

        old_chunks: List[CodeBlock] = []
        new_chunks: List[CodeBlock] = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            old_part = "".join(tok for tok in old_tokens[i1:i2])
            new_part = "".join(tok for tok in new_tokens[j1:j2])

            if tag == "equal":
                if old_part:
                    old_chunks.append(CodeBlock(content=old_part))
                    new_chunks.append(CodeBlock(content=old_part))
            elif tag == "replace":
                if old_part:
                    old_chunks.append(CodeBlock(content=old_part, color="diffcharred"))
                if new_part:
                    new_chunks.append(CodeBlock(content=new_part, color="diffchargreen"))
            elif tag == "delete":
                if old_part:
                    old_chunks.append(CodeBlock(content=old_part, color="diffcharred"))
            elif tag == "insert":
                if new_part:
                    new_chunks.append(CodeBlock(content=new_part, color="diffchargreen"))

        return old_chunks, new_chunks

    def _flush_hunk(self, hunk: List[str], line_start: int = 1) -> List[Line]:
        old_lineno = line_start
        new_lineno = line_start
        paired = []

        deletions = [line[1:].rstrip() for line in hunk if line.startswith("-")]
        additions = [line[1:].rstrip() for line in hunk if line.startswith("+")]
        max_len = max(len(deletions), len(additions))

        for i in range(max_len):
            old_line = deletions[i] if i < len(deletions) else ""
            new_line = additions[i] if i < len(additions) else ""

            if old_line and new_line:
                old_diff, new_diff = self._inline_diff(old_line, new_line)
                paired.append(
                    Line(
                        content=(
                            Cell(content=old_diff, line_nr=old_lineno, color="remred"),
                            Cell(content=new_diff, line_nr=new_lineno, color="addgreen"),
                        )
                    )
                )
                old_lineno += 1
                new_lineno += 1
            elif old_line:
                paired.append(
                    Line(
                        content=(
                            Cell(
                                content=[CodeBlock(content=old_line)],
                                line_nr=old_lineno,
                            ),
                            Cell(content=[], line_nr=None),
                        )
                    )
                )
                old_lineno += 1
            elif new_line:
                paired.append(
                    Line(
                        content=(
                            Cell(content=[], line_nr=None),
                            Cell(
                                content=[CodeBlock(content=new_line)],
                                line_nr=new_lineno,
                            ),
                        )
                    )
                )
                new_lineno += 1
        return paired

    def parse_diff_lines(self) -> List[Line]:
        line_nr = 1
        hunk = []
        
        self._clean_diff_file()
        for line in self.srclines:
            if line.startswith("-") or line.startswith("+"):
                hunk.append(line)
            else:
                if hunk:
                    self._lines.extend(self._flush_hunk(hunk, line_nr))
                    hunk = []

                content = line[1:].rstrip() if line.startswith(" ") else line.rstrip()
                self._lines.append(
                    Line(
                        content=(
                            Cell(content=[CodeBlock(content=content)], line_nr=line_nr),
                            Cell(content=[CodeBlock(content=content)], line_nr=line_nr),
                        )
                    )
                )
                line_nr += 1

        if hunk:
            self._lines.extend(self._flush_hunk(hunk))

        return self._lines
