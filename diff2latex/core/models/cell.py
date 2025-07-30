from pydantic import BaseModel, Field, PrivateAttr
from typing import List
from . import CodeBlock
from ..utils import ColorMap


class Cell(BaseModel):
    """
    Base class for all cells in the diff2latex table.
    """

    content: List[CodeBlock] = Field(..., description="The content of the cell.")
    line_nr: int | None = Field(..., description="Line number in the diff.")
    bg_color: str | None = Field(None, description="Color of the cell, if applicable.")
    _colormap: ColorMap | None = PrivateAttr(default=None)

    def attach_colormap(self, colormap: ColorMap) -> "Cell":
        """
        Create a new Cell with colorized code blocks using the provided colormap.
        """
        if not colormap or not colormap.root:
            return self

        it = iter(colormap.root)
        new_content = []

        for code_block in self.content:
            new_code_block = (
                [next(it) for _ in code_block.content] if code_block.content else []
            )

            new_content.append(
                CodeBlock(
                    content=code_block.content,
                    bg_color=code_block.bg_color,
                    colormap=ColorMap(root=new_code_block),
                )
            )

        return Cell(
            content=new_content,
            line_nr=self.line_nr,
            bg_color=self.bg_color,
            _colormap=colormap,
        )

    def to_latex(self) -> str:
        """
        Convert the cell content to LaTeX format.
        """
        if self.bg_color:
            return (
                f"\\cellcolor{{{self.bg_color}}}{self.line_nr} & \\cellcolor{{{self.bg_color}}}"
                + "".join(f"{code.to_latex()}" for code in self.content)
            )
        return f"{self.line_nr} & " + "".join(
            f"{code.to_latex()}" for code in self.content
        )

    def add_code_block(self, code_block: CodeBlock) -> None:
        """
        Add a code block to the cell.
        """
        self.content.append(code_block)
