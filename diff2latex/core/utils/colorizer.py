from typing import List, Tuple
from pydantic import BaseModel, Field
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
from .colormap import ColorMap


class CharColorizer(BaseModel):
    style_name: str | None = Field(description="Pygments style to use for coloring.")

    def _get_style(self):
        if not self.style_name:
            return None
        return get_style_by_name(self.style_name)

    @staticmethod
    def _get_token_colors(style):
        return {
            token: f"{style.styles[token]}" if style.styles[token] else "#000000"
            for token in style.styles
        }

    @staticmethod
    def _resolve_color(ttype, token_colors):
        while ttype not in token_colors:
            ttype = ttype.parent
        return token_colors.get(ttype, "#000000")

    def get_colormap(self, code: str) -> "ColorMap | None":
        style = self._get_style()
        if style is None:
            return None
        token_colors = self._get_token_colors(style)
        char_colors: List[Tuple[str, str]] = []
        for ttype, value in lex(code, PythonLexer()):
            color = self._resolve_color(ttype, token_colors)
            for char in value:
                if char != '\n':
                    char_colors.append((char, color))
        return ColorMap(root=char_colors)
