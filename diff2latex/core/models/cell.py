from pydantic import BaseModel, Field, model_validator
from typing import List, Any
from . import CodeBlock
from ..utils import ColorMap, CharColorizer


class Cell(BaseModel):
    """
    Base class for all cells in the diff2latex table.
    """

    content: List[CodeBlock] = Field(..., description="The content of the cell.")
    line_nr: int | None = Field(..., description="Line number in the diff.")
    color: str | None = Field(None, description="Color of the cell, if applicable.")
    colormap: ColorMap | None = Field(
        None, description="The color map for the text in the code block."
    )

    def _rebuild_colorized_content(self) -> None:
        """
        Rebuild the content of the cell with colorized code blocks.
        """
        it = iter(self.colormap.root)
        new_content = []

        for code_block in self.content:
            new_code_block = [next(it) for _ in code_block.content] if self.colormap.root else []
            new_content.append(
                CodeBlock(
                    content=code_block.content,
                    color=code_block.color,
                    txtcolormap=ColorMap(root=new_code_block),
                )
            )
        self.content = new_content    

    def to_latex(self, highlight: bool = False) -> str:
        """
        Convert the cell content to LaTeX format.
        """
        if self.colormap:
            self._rebuild_colorized_content()

        if self.color:
            return (
                f"\\cellcolor{{{self.color}}}{self.line_nr} & \\cellcolor{{{self.color}}}"
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
