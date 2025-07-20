from pydantic import BaseModel, Field
from typing import Tuple
from .cell import Cell


class Line(BaseModel):
    """
    Abstract base class for lines in a diff.
    """

    content: Tuple[Cell, Cell] = Field(
        ...,
        description="The content of the line, consisting of two cells: old and new.",
    )

    def to_latex(self) -> str:
        """
        Convert the line to its LaTeX representation.
        """
        old_cell, new_cell = self.content
        return f"{old_cell.to_latex()} & {new_cell.to_latex()} \\\\"
