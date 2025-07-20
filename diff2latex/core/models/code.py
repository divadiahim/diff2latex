from pydantic import BaseModel, Field


class CodeBlock(BaseModel):
    """
    Represents a code block with optional language and content.
    """

    content: str = Field(..., description="The content of the code block.")
    color: str | None = Field(
        None, description="The color of the box around the code block."
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
        if self.color:
            return f"\\boxx{{{self.color}}}{{{self._sanitize(self.content)}}}"
        return f"\\code{{{self._sanitize(self.content)}}}"
