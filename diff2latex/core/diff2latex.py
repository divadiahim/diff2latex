# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false
from pydantic import BaseModel, PrivateAttr
from typing import TextIO
from .models import Line, Cell, CodeBlock
from .utils import CharColorizer
from difflib import SequenceMatcher
import re


class Diff2Latex(BaseModel):
    _parsed_lines: list[Line] = PrivateAttr(default_factory=list)
    colorizer: CharColorizer

    @staticmethod
    def _clean_diff_file(lines: list[str]) -> list[str]:
        return [line for line in lines if not line.startswith(("---", "+++", "@@"))]

    @staticmethod
    def _tokenize(line: str) -> list[str]:
        return re.findall(r"\s+|\w+|[^\w\s]", line)


    def _inline_diff(self, old_line: str, new_line: str) -> tuple[list[CodeBlock], list[CodeBlock]]:
        old_tokens = self._tokenize(old_line)
        new_tokens = self._tokenize(new_line)
        matcher = SequenceMatcher(None, old_tokens, new_tokens)

        old_chunks = []
        new_chunks = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            old_part = "".join(old_tokens[i1:i2])
            new_part = "".join(new_tokens[j1:j2])

            if tag == "equal":
                old_chunks.append(CodeBlock(content=old_part))
                new_chunks.append(CodeBlock(content=old_part))
            elif tag == "replace":
                if old_part:
                    old_chunks.append(CodeBlock(content=old_part, bg_color="diffcharred"))
                if new_part:
                    new_chunks.append(CodeBlock(content=new_part, bg_color="diffchargreen"))
            elif tag == "delete":
                old_chunks.append(CodeBlock(content=old_part, bg_color="diffcharred"))
            elif tag == "insert":
                new_chunks.append(CodeBlock(content=new_part, bg_color="diffchargreen"))

        return old_chunks, new_chunks

    def _process_hunk(self, hunk: list[str], line_start: int = 1) -> list[Line]:
        deletions = [line[1:].rstrip() for line in hunk if line.startswith("-")]
        additions = [line[1:].rstrip() for line in hunk if line.startswith("+")]
        max_len = max(len(deletions), len(additions))

        lines = []
        old_lineno = line_start
        new_lineno = line_start

        for i in range(max_len):
            old_line = deletions[i] if i < len(deletions) else ""
            new_line = additions[i] if i < len(additions) else ""
            
            old_line_colormap = self.colorizer.get_colormap(old_line)
            new_line_colormap = self.colorizer.get_colormap(new_line)

            if old_line and new_line:
                old_diff, new_diff = self._inline_diff(old_line, new_line)
                lines.append(Line(
                    content=(
                        Cell(content=old_diff, line_nr=old_lineno, bg_color="remred").attach_colormap(old_line_colormap),
                        Cell(content=new_diff, line_nr=new_lineno, bg_color="addgreen").attach_colormap(new_line_colormap)
                    ),
                ))
                old_lineno += 1
                new_lineno += 1
            elif old_line:
                lines.append(Line(
                    content=(
                        Cell(content=[CodeBlock(content=old_line)], line_nr=old_lineno, bg_color="remred").attach_colormap(old_line_colormap),
                        Cell(content=[], line_nr=None)
                    ),
                ))
                old_lineno += 1
            elif new_line:
                lines.append(Line(
                    content=(
                        Cell(content=[], line_nr=None),
                        Cell(content=[CodeBlock(content=new_line)], line_nr=new_lineno, bg_color="addgreen").attach_colormap(new_line_colormap)
                    ),
                ))
                new_lineno += 1

        return lines

    def parse(self, lines: list[str]) -> None:
        clean_lines = self._clean_diff_file(lines)
        hunk: list[str] = []
        line_nr = 1

        for line in clean_lines:
            if line.startswith(("-", "+")):
                hunk.append(line)
            else:
                if hunk:
                    self._parsed_lines.extend(self._process_hunk(hunk, line_nr))
                    hunk = []

                line = line[1:].rstrip() if line.startswith(" ") else line.rstrip()
                line_colormap = self.colorizer.get_colormap(line)

                self._parsed_lines.append(Line(
                    content=(
                        Cell(content=[CodeBlock(content=line)], line_nr=line_nr).attach_colormap(line_colormap),    
                        Cell(content=[CodeBlock(content=line)], line_nr=line_nr).attach_colormap(line_colormap)
                    ),
                ))
                line_nr += 1

        if hunk:
            self._parsed_lines.extend(self._process_hunk(hunk, line_nr))

    @classmethod
    def build(cls, file: TextIO, colorizer: CharColorizer) -> "Diff2Latex":
        instance = cls(colorizer=colorizer)
        instance.parse(file.readlines())
        return instance

    def to_latex(self) -> str:
        if not self._parsed_lines:
            raise ValueError("No lines to convert to LaTeX.")

        return "\n".join(line.to_latex() for line in self._parsed_lines)
