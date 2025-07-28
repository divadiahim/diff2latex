from pydantic import BaseModel, Field
from itertools import groupby
from operator import itemgetter
from ..utils import ColorMap


class CodeBlock(BaseModel):
    """
    Represents a code block with optional language and content.
    """

    content: str = Field(..., description="The content of the code block.")
    color: str | None = Field(
        None, description="The color of the box around the code block."
    )
    colormap: ColorMap | None = Field(
        None, description="The color map for the text in the code block."
    )

    def _sanitize(self, s: str) -> str:
        """Sanitize string for LaTeX."""
        return (
            s.replace("\\", "\\textbackslash")
            .replace("%", "\\%")
            .replace("$", "\\$")
            .replace("&", "\\&")
            .replace(" ", "\\ ")
            .replace("_", "\\_")
            .replace("{", "\\{")
            .replace("}", "\\}")
            .replace("#", "\\#")
            .replace("~", "\\~")
        )

    def to_latex(self) -> str:
        """
        Convert the code block to its LaTeX representation.
        """
        if self.colormap:
            latex_content = []
            groups = [list(g) for k, g in groupby(self.colormap.root, key=itemgetter(1))]
            for group in groups:
                content = "".join(char for char, _ in group)
                color = group[0][1]
                latex_content.append(f"\\code{{{color.strip('#')}}}{{{self._sanitize(content)}}}")
            return "".join(latex_content)
                
        
        if self.color:
            return f"\\boxx{{{self.color}}}{{{self._sanitize(self.content)}}}"
        return f"\\code{{{'FF5733'}}}{{{self._sanitize(self.content)}}}"
