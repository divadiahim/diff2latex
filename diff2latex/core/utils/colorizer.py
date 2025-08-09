# pyright:basic
# ^ cuz pygments have not type hinted their shit and my ide is crying
from pydantic import BaseModel, Field
from pygments import lex
from pygments.lexers import PythonLexer, CppLexer, JavaLexer, HaskellLexer
from pygments.styles import get_style_by_name  
from .colormap import ColorMap


class CharColorizer(BaseModel):
    style_name: str | None = Field(description="Pygments style to use for coloring.")
    ext: str | None = Field(default=None, description="File extension to determine lexer.")

    def _get_lexer(self):
        if not self.ext:
            return CppLexer() # default
            
        ext_map = {
            '.py': PythonLexer(),
            '.cpp': CppLexer(),
            '.c': CppLexer(),
            '.cc': CppLexer(),
            '.cxx': CppLexer(),
            '.h': CppLexer(),
            '.hpp': CppLexer(),
            '.java': JavaLexer(),
            '.hs': HaskellLexer(), 
        }
        
        return ext_map.get(self.ext.lower(), PythonLexer())

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
        char_colors = []
        lexer = self._get_lexer()
        for ttype, value in lex(code, lexer):
            color = self._resolve_color(ttype, token_colors)
            for char in value:
                if char != '\n':
                    char_colors.append((char, color[color.find('#'):].strip("#"))) # Temp solution to remove the text attibutes
        return ColorMap(root=char_colors)
