from pydantic import BaseModel, Field
from typing import List
from . import CodeBlock


class Cell(BaseModel):
    """
    Base class for all cells in the diff2latex table.
    """

    content: List[CodeBlock] = Field(..., description="The content of the cell.")
    line_nr: int | None = Field(..., description="Line number in the diff.")
    color: str | None = Field(None, description="Color of the cell, if applicable.")

    def to_latex(self) -> str:
        """
        Convert the cell content to LaTeX format.
        """
        if self.color:
            return f"\\cellcolor{{{self.color}}}{self.line_nr} & " + "".join(
                f"{code.to_latex()}" for code in self.content
            )
        return f"{self.line_nr} & " + "".join(f"{code.to_latex()}" for code in self.content)

    def add_code_block(self, code_block: CodeBlock) -> None:
        """
        Add a code block to the cell.
        """
        self.content.append(code_block)
